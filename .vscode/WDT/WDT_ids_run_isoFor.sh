IDS=/home/spice/2ndIDS/BA_ids/ipal-iids
OUT=/home/spice/WDT/ids_isoFor_out
IN=/home/spice/WDT
CONFIG=/home/spice/2ndIDS/BA_ids/.vscode/WDT

for filename in $CONFIG/IsoForConfigs/*; do
    echo "starting attack1 with config: $config" >> $OUT/bash.log; 
    # attack1
    $IDS \
        --train.ipal $IN/normal.out \
        --live.ipal $IN/attack_1.out \
        --output $OUT/res_attack1_$(basename $filename).out \
        --config $CONFIG/IsoForConfigs/$(basename $filename) \
        --combiner.config $CONFIG/wdt_combiner.config \
        --log INFO \
        --logfile $OUT/res_attack1_$(basename $filename).log \
        --retrain;

    echo "starting attack2 with config: $config" >> $OUT/bash.log; 
    # attack2
    $IDS \
        --train.ipal $IN/normal.out \
        --live.ipal $IN/attack_2.out \
        --output $OUT/res_attack2_$(basename $filename).out \
        --config $CONFIG/IsoForConfigs/$(basename $filename) \
        --combiner.config $CONFIG/wdt_combiner.config \
        --log INFO \
        --logfile $OUT/res_attack2_$(basename $filename).log;

    echo "starting attack3 with config: $config" >> $OUT/bash.log; 
    #attack3
    $IDS \
        --train.ipal $IN/normal.out \
        --live.ipal $IN/attack_3.out \
        --output $OUT/res_attack3_$(basename $filename).out \
        --config $CONFIG/IsoForConfigs/$(basename $filename) \
        --combiner.config $CONFIG/wdt_combiner.config \
        --log INFO \
        --logfile $OUT/res_attack3_$(basename $filename).log;

    echo "starting attack4 with config: $config" >> $OUT/bash.log; 
    #attack4
    $IDS \
        --train.ipal $IN/normal.out \
        --live.ipal $IN/attack_4.out \
        --output $OUT/res_attack4_$(basename $filename).out \
        --config $CONFIG/IsoForConfigs/$(basename $filename) \
        --combiner.config $CONFIG/wdt_combiner.config \
        --log INFO \
        --logfile $OUT/res_attack4_$(basename $filename).log;
done