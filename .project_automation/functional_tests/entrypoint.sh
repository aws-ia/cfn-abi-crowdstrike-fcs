#!/bin/bash -ex


## NOTE: paths may differ when running in a managed task. To ensure behavior is consistent between
# managed and local tasks always use these variables for the project and project type path
PROJECT_PATH=${BASE_PATH}/project
PROJECT_TYPE_PATH=${BASE_PATH}/projecttype
export REGION=$(grep -A1 regions: .taskcat.yml | awk '/ - / {print $NF}' |sort | uniq -c |sort -k1| head -1 |awk '{print $NF}')

cd ${PROJECT_PATH}

cleanup_region() {
    echo "Cleanup running in region: $1"
    export AWS_DEFAULT_REGION=$1
    python3 scripts/cleanup_config.py -C scripts/cleanup_config.json
}

cleanup_all_regions() {
    export AWS_DEFAULT_REGION=$REGION
    regions=($(aws ec2 describe-regions --query "Regions[*].RegionName" --output text))
    for region in ${regions[@]}
    do
        cleanup_region ${region}
    done
}

run_test() {
    cleanup_all_regions
    unset AWS_DEFAULT_REGION
    if [ -z "$1" ]; then
        echo "Running e2e test: ALL"
        taskcat test run -n
        .project_automation/functional_tests/scoutsuite/scoutsuite.sh
    else
        echo "Running e2e test: $1"
        taskcat test run -n -t $1
        .project_automation/functional_tests/scoutsuite/scoutsuite.sh
    fi
}

# Run taskcat e2e test
run_test "cw-test"

run_test "cw-test-ct"

run_test "cw-test-ssm"

run_test "cw-test-all"

## Executing ash tool

#find ${PROJECT_PATH} -name lambda.zip -exec rm -rf {} \;

#git clone https://github.com/aws-samples/automated-security-helper.git /tmp/ash

# Set the repo path in your shell for easier access
#export PATH=$PATH:/tmp/ash

#ash --source-dir .
#cat aggregated_results.txt
