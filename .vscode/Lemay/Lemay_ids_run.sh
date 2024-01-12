#!/bin/bash
IDS=/home/sj/BA_stuff/BA_ids/ipal-iids
OUT=/home/sj/BA_stuff/transcribed_pcaps/Lemay/ids_out
IN=/home/sj/BA_stuff/transcribed_pcaps/Lemay
CONFIG=/home/sj/BA_stuff/BA_ids/.vscode/Lemay

for filename in $CONFIG/ids-configs/*; do
    # Characterization
    echo "starting characterization with config" >> $OUT/bash.log;
    echo $filename >> $OUT/bash.log
    $IDS \
        --train.ipal $IN/normal/run1_6rtu.pcap.out \
        --live.ipal $IN/attack/characterization_modbus_6RTU_with_operate.out \
        --output $OUT/characterization_$(basename $filename).out \
        --config $CONFIG/ids-configs/$(basename $filename) \
        --combiner.config $CONFIG/Lemay_combiner.config \
        --log INFO \
        --logfile $OUT/characterization_$(basename $filename).log \
        --retrain;

    # CNC Upload
    echo "starting CnC Upload with config" >> $OUT/bash.log;
    echo $filename >> $OUT/bash.log;
    $IDS \
        --train.ipal $IN/normal/run1_6rtu.pcap.out \
        --live.ipal $IN/attack/CnC_uploading_exe_modbus_6RTU_with_operate.out \
        --output $OUT/CnC_upload_$(basename $filename).out \
        --config $CONFIG/ids-configs/$(basename $filename) \
        --combiner.config $CONFIG/Lemay_combiner.config \
        --log INFO \
        --logfile $OUT/CnC_upload_$(basename $filename).log;

    echo "starting exploit with config:" >> $OUT/bash.log;
    echo $filename >> $OUT/bash.log;
    # exploit
    $IDS \
        --train.ipal $IN/normal/run1_6rtu.pcap.out \
        --live.ipal $IN/attack/exploit_ms08_netapi_modbus_6RTU_with_operate.out \
        --output $OUT/exploit_$(basename $filename).out \
        --config $CONFIG/ids-configs/$(basename $filename) \
        --combiner.config $CONFIG/Lemay_combiner.config \
        --log INFO \
        --logfile $OUT/exploit_$(basename $filename).log;

    echo "starting moving files with config:" >> $OUT/bash.log; 
    echo $filename >> $OUT/bash.log;
    # moving files
    $IDS \
        --train.ipal $IN/normal/run1_6rtu.pcap.out \
        --live.ipal $IN/attack/moving_two_files_modbus_6RTU.out \
        --output $OUT/moving_files_$(basename $filename).out \
        --config $CONFIG/ids-configs/$(basename $filename) \
        --combiner.config $CONFIG/Lemay_combiner.config \
        --log INFO \
        --logfile $OUT/moving_files_$(basename $filename).log;

    echo "starting fake command with config:" >> $OUT/bash.log; 
    echo $filename >> $OUT/bash.log;
    # fake command
    $IDS \
        --train.ipal $IN/normal/run1_6rtu.pcap.out \
        --live.ipal $IN/attack/send_a_fake_command_modbus_6RTU_with_operate.out \
        --output $OUT/fake_command_$(basename $filename).out \
        --config $CONFIG/ids-configs/$(basename $filename) \
        --combiner.config $CONFIG/Lemay_combiner.config \
        --log INFO \
        --logfile $OUT/fake_command_$(basename $filename).log;
done