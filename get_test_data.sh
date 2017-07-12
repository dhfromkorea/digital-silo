USER_ID="$1"
TEST_DATA_PATH="src/test_data/"
PISA_IP="164.67.183.180"
ssh "$USER_ID@$PISA_IP" << EOF
  cd /Rosenthal
  find . -path ./cuts -prune -o -name "*.cuts" -print > /tmp/cuts.txt
  # get the list of paths
EOF
mkdir data
cd data
rsync -avhW --no-compress --progress "$USER_ID@$PISA_IP:/tmp/cuts.txt" .
sed -e 's/.cuts/.txt3/g' cuts.txt > cuts_captions.txt
sed -e 's/.cuts/.mp4/g' cuts.txt > cuts_videos.txt
rsync -avhW --no-compress --progress --files-from=cuts.txt "$USER_ID@$PISA_IP:/Rosenthal/" .
rsync -avhW --no-compress --progress --files-from=cuts_captions.txt "$USER_ID@$PISA_IP:/Rosenthal/" .
rsync -avhW --no-compress --progress --files-from=cuts_videos.txt "$USER_ID@$PISA_IP:/Rosenthal/" .
