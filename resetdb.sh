#!/bin/sh

DBNAME='mutodb'
sudo -u postgres dropdb $DBNAME
sudo -u postgres createdb $DBNAME
sudo -u postgres psql <<EOF
GRANT ALL PRIVILEGES ON DATABASE $DBNAME TO muuser
EOF

# migrate our django apps
APPS="mutopia update"
python manage.py migrate
for app in $APPS ; do
    echo $app
    python manage.py makemigrations $app
    python manage.py migrate $app
done

# and load their fixtures
LOAD="python manage.py loaddata"
MUTOPIA_MODELS="                                \
  Composer                                      \
  Contributor                                   \
  Style                                         \
  Instrument                                    \
  LPVersion                                     \
  License                                       \
"

UPDATE_MODELS="                                 \
  InstrumentMap                                 \
  Marker                                        \
"

# these depend on previous mutopia models
LAST_MODELS="                                   \
  Piece                                         \
  Collection                                    \
  AssetMap                                      \
"

for t in $MUTOPIA_MODELS; do
    $LOAD mutopia/fixtures/${t}.json
done

for t in $UPDATE_MODELS; do
    $LOAD update/fixtures/${t}.json
done

for t in $LAST_MODELS; do
    $LOAD mutopia/fixtures/${t}.json
done
