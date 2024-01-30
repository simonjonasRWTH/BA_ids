import joblib
from sklearn.svm import OneClassSVM
from sklearn.model_selection import GridSearchCV

import ipal_iids.settings as settings
from ids.featureids import FeatureIDS


class OCSVM(FeatureIDS):
    _name = "OCSVM"
    _description = "One Class SVM forest classifier."
    _svm_default_settings = {
        # OCSVM GridSearch Parameters
        "kernel": ["rbf", "linear", "sigmoid", "poly"],
        "degree": [3],
        "gamma": [1, 0.1, 0.01, 0.001, "auto", "scale"],
        "coef0": [0.0],
        "shrinking": [True],
        "nu": [0.5],
        "tol": [0.001],
        "cache_size": [1024],
        "max_iter": [-1],
        # GridSearch Options
        "scoring": None,  # accuracy ..
        "jobs": 4,
        "verbose": 10,
    }

    def __init__(self, name=None):
        super().__init__(name=name)
        self._add_default_settings(self._svm_default_settings)

        self.ocsvm = None

    # the IDS is given the path to file(s) containing its requested training data
    def train(self, ipal=None, state=None):
        if ipal and state:
            settings.logger.error("Only state or message supported")
            exit(1)

        if state is None:
            state = ipal

        events, _, _ = super().train(state=state)

        # Learn SVM
        settings.logger.info("Learning OCSVM")
        tuned_parameters = {
            "kernel": self.settings["kernel"],
            "degree": self.settings["degree"],
            "gamma": self.settings["gamma"],
            "coef0": self.settings["coef0"],
            "shrinking": self.settings["shrinking"],
            "nu": self.settings["nu"],
            "tol": self.settings["tol"],
            "cache_size": self.settings["cache_size"],
            "max_iter": self.settings["max_iter"],
        }
        settings.logger.info(tuned_parameters)

        # Test if gridsearch is neccesary
        if max([len(v) for v in tuned_parameters.values()]) > 1:
            settings.logger.info("Finding best parameteres with GirdSearchCV")
            svc = GridSearchCV(
                OneClassSVM(),
                [tuned_parameters],
                scoring=self.settings["scoring"],
                n_jobs=self.settings["jobs"],
                verbose=self.settings["verbose"],
            )

            svc.fit(events)

            settings.logger.info("Best parameters set found on development set:")
            settings.logger.info(svc.best_params_)
            settings.logger.info("Grid scores on development set:")
            means = svc.cv_results_["mean_test_score"]
            stds = svc.cv_results_["std_test_score"]
            for mean, std, params in zip(means, stds, svc.cv_results_["params"]):
                settings.logger.info(
                    "%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params)
                )

            # Save best estimator
            self.ocsvm = svc.best_estimator_

        else:
            tuned_parameters = {k: v[0] for k, v in tuned_parameters.items()}
            self.ocsvm = OneClassSVM(**tuned_parameters)
            self.ocsvm.fit(events)

    def new_state_msg(self, msg):
        state = super().new_state_msg(msg)
        if state is None:
            return False, None

        alert = bool(self.ocsvm.predict([state])[0])

        return alert, 1 if alert else 0

    def new_ipal_msg(self, msg):
        # There is no difference for this IDS in state or message format! It only depends on the configuration which features are used.
        return self.new_state_msg(msg)

    def save_trained_model(self):
        if self.settings["model-file"] is None:
            return False

        model = {
            "_name": self._name,
            "preprocessors": super().save_trained_model(),
            "settings": self.settings,
            "classifier": self.svm,
            "classes": self.classes,
        }

        joblib.dump(model, self._resolve_model_file_path(), compress=3)

        return True

    def load_trained_model(self):
        if self.settings["model-file"] is None:
            return False

        try:  # Open model file
            model = joblib.load(self._resolve_model_file_path())
        except FileNotFoundError:
            settings.logger.info(
                "Model file {} not found.".format(str(self._resolve_model_file_path()))
            )
            return False

        # Load model
        assert self._name == model["_name"]
        super().load_trained_model(model["preprocessors"])
        self.settings = model["settings"]
        self.svm = model["classifier"]
        self.classes = model["classes"]

        return True
