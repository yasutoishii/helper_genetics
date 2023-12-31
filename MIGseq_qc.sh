RAW_DATA_DIR=../fastq                            ## Dir containing demultiplexed fastqs
ADAPTOR_CUT_PE_PAIRED_DIR=paired_cutonly         ## Dir to contain   paired reads after adaptors are cut.
ADAPTOR_CUT_PE_UNPAIRED_DIR=unpaired_cutonly     ## Dir to contain unpaired reads after adaptors are cut.
QC_PE_PAIRED_DIR=paired_qcPE_100bp               ## Dir to contain   paired reads after adapting quality filtering to ADAPTOR_CUT_PE_PAIRED_DIR
QC_PE_UNPAIRED_DIR=unpaired_qcPE_100bp           ## Dir to contain unpaired reads after adapting quality filtering to ADAPTOR_CUT_PE_PAIRED_DIR
QC_SE_DIR=unpaired_qcSE_100bp                    ## Dir to contain unpaired reads after adapting quality filtering to ADAPTOR_CUT_PE_UNPAIRED_DIR
QC_ALL_DIR=qc_all_100bp                          ## Dir to contain all quality-filtered fastqs
LOG_DIR=trim_log_100bp                           ## Dir to contain log files

N_THREADS=15                                     ## Specify No of threads
OUTPUT_LEN=100                                   ## How long do you cut after quality filtering [bp]
TRIMMOMATIC_PATH=path/to/your/trimmomatic/trimmomatic-\*.\*\*.jar   ### Specify your path to trimmomatic

mkdir -p ${ADAPTOR_CUT_PE_PAIRED_DIR}
mkdir -p ${ADAPTOR_CUT_PE_UNPAIRED_DIR}
mkdir -p ${QC_PE_PAIRED_DIR}
mkdir -p ${QC_PE_UNPAIRED_DIR}
mkdir -p ${QC_SE_DIR}
mkdir -p ${QC_ALL_DIR}
mkdir -p ${LOG_DIR}

### Trimming the adaptor                                  ###
### The sufix is for paired-end data demultiplexed by BGI ###
for f in `ls ${RAW_DATA_DIR}|grep _1.fq.gz|sed -e 's/_1.fq.gz$//g'`;
do
    echo ${f};
    java -jar ${TRIMMOMATIC_PATH} \
        PE \
        -threads ${N_THREADS} \
        -phred33 \
        -trimlog ${LOG_DIR}/${f}_adaptor_cut.log \
        ${RAW_DATA_DIR}/${f}_1.fq.gz \
        ${RAW_DATA_DIR}/${f}_2.fq.gz \
        ${ADAPTOR_CUT_PE_PAIRED_DIR}/${f}.1.fastq.gz \
        ${ADAPTOR_CUT_PE_UNPAIRED_DIR}/${f}.1.fastq.gz \
        ${ADAPTOR_CUT_PE_PAIRED_DIR}/${f}.2.fastq.gz \
        ${ADAPTOR_CUT_PE_UNPAIRED_DIR}/${f}.2.fastq.gz \
        ILLUMINACLIP:MIGadapter.fasta:2:30:10;
done


### Quality filtering ###
for f in `ls ${RAW_DATA_DIR}|grep _1.fq.gz|sed -e 's/_1.fq.gz$//g'`;
do
    echo ${f};
    java -jar ${TRIMMOMATIC_PATH} \
        PE \
        -threads ${N_THREADS} \
        -phred33 \
        -trimlog ${LOG_DIR}/${f}_qcPE.log \
        ${ADAPTOR_CUT_PE_PAIRED_DIR}/${f}.1.fastq.gz \
        ${ADAPTOR_CUT_PE_PAIRED_DIR}/${f}.2.fastq.gz \
        ${QC_PE_PAIRED_DIR}/${f}.1.fastq.gz \
        ${QC_PE_UNPAIRED_DIR}/${f}.1.fastq.gz \
        ${QC_PE_PAIRED_DIR}/${f}.2.fastq.gz \
        ${QC_PE_UNPAIRED_DIR}/${f}.2.fastq.gz \
        SLIDINGWINDOW:4:15 \
        CROP:${OUTPUT_LEN} MINLEN:${OUTPUT_LEN};
done

for f in `ls ${RAW_DATA_DIR}|grep _1.fq.gz|sed -e 's/_1.fq.gz$//g'`;
do
    echo ${f};
    java -jar ${TRIMMOMATIC_PATH} \
        SE \
        -threads ${N_THREADS} \
        -phred33 \
        -trimlog ${LOG_DIR}/${f}_qcSE_1.log \
        ${ADAPTOR_CUT_PE_UNPAIRED_DIR}/${f}.1.fastq.gz \
        ${QC_SE_DIR}/${f}.1.fastq.gz \
        SLIDINGWINDOW:4:15 \
        CROP:${OUTPUT_LEN} MINLEN:${OUTPUT_LEN};

    java -jar /home/chibalab/Analyse/Trimmomatic-0.39/trimmomatic-0.39.jar \
        SE \
        -threads ${N_THREADS} \
        -phred33 \
        -trimlog ${LOG_DIR}/${f}_qcSE_2.log \
        ${ADAPTOR_CUT_PE_UNPAIRED_DIR}/${f}.2.fastq.gz \
        ${QC_SE_DIR}/${f}.2.fastq.gz \
        SLIDINGWINDOW:4:15 \
        CROP:${OUTPUT_LEN} MINLEN:${OUTPUT_LEN};
done

### Mergining all reads ###
for f in `ls ${RAW_DATA_DIR}|grep _1.fq.gz|sed -e 's/_1.fq.gz$//g'`;
do
    cat ${QC_PE_PAIRED_DIR}/${f}.1.fastq.gz ${QC_PE_UNPAIRED_DIR}/${f}.1.fastq.gz \
        ${QC_PE_PAIRED_DIR}/${f}.2.fastq.gz ${QC_PE_UNPAIRED_DIR}/${f}.2.fastq.gz \
        ${QC_SE_DIR}/${f}.1.fastq.gz        ${QC_SE_DIR}/${f}.2.fastq.gz \
        > ${QC_ALL_DIR}/${f}.fastq.gz
done