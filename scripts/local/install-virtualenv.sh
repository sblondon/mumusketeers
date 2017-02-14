#! /bin/bash


PYTHON=python3.5
WHEEL_DIR=${HOME}/.pip/wheelhouse
REQUIREMENTS=../../requirements.txt
PYPI_YAAL="https://${PIP_YAAL_USER}:${PIP_YAAL_PASSWORD}@pypi.yaal.fr/yaal/prod/+simple/"


rm -rf local.virtualenv
${PYTHON} -m venv local.virtualenv

cd ./local.virtualenv/bin/
./pip install --upgrade wheel

{
        ./pip install --requirement ${REQUIREMENTS} --no-index --find-links "file://${WHEEL_DIR}"
} || {
        # "raté on installe wheel"
        ./pip install --upgrade setuptools --index-url "${PYPI_YAAL}"
        # "on tente de construire les wheel en les récupérant depuis trois"
        # "le --find-links file://$wheel_dir sert à ne pas reconstruire les paquets déja compilés"
        ./pip wheel --requirement ${REQUIREMENTS} -w "${WHEEL_DIR}" --find-links "file://${WHEEL_DIR}" --index-url "${PYPI_YAAL}"
        # echo "on retente une install"
        ./pip install --requirement ${REQUIREMENTS} --no-index --find-links "file://${WHEEL_DIR}"
}

