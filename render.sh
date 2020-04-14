VOL=/docs
IMG=rmd-renderer
docker build -t $IMG . 
DOCS=$VOL docker run -it -v $(pwd):$VOL $IMG
