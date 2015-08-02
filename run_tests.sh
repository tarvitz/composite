#!/bin/bash
ALLURE=`which allure`
COV=`which coverage`
PYTHONPATH=$PWD $COV run --source=composite -m py.test --alluredir=reports/allure
STATUS=$?
if [ ! -z $ALLURE ]; then
    echo "allure found"
    if [ ! $STATUS -eq 0 ]; then
        echo "building allure reports"
        $ALLURE generate generate reports/allure/ -o reports/reports -v 1.4.15
    fi
fi
