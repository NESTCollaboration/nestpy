#  This script is used for syncing to the NEST main repository
#  to ensure that the bindings bind to the same version of NEST

export VERSION=`python -c "import nestpy;print(nestpy.__nest_version__)"`
echo $VERSION 

git clone https://github.com/NESTCollaboration/nest.git nest_source
cd nest_source
git fetch --all --tags --prune
git checkout tags/v${VERSION} -b test
cd ..

cd src/nestpy
for filename in *.{cpp,hh}; do
    export REPO_FILE=`find ../../nest_source/ -name ${filename}`
    if [ ! -z "$REPO_FILE" -a "$REPO_FILE" != " " ]; then
        cp $REPO_FILE $filename
    fi
    
done
cd ../..
#rm -Rf nest_source
#git commit -m "Sync with $VERSION" -a
