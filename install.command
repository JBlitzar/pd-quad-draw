#!/bin/bash
cd "$(dirname "$0")"

while ! ls -1 /Volumes | grep -q CIRCUITPY; do
    sleep 1
done

sleep 2

rm /Volumes/CIRCUITPY/*.bin  # clear up space before copying over
rm /Volumes/CIRCUITPY/img.txt  # clear up space before copying over
cp pd-src/*.py /Volumes/CIRCUITPY/
cp pd-src/*.txt /Volumes/CIRCUITPY/

# lib files
cp -R pd-src/lib/* /Volumes/CIRCUITPY/lib/

echo "Done! Files copied to CIRCUITPY"
