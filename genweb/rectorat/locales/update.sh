#|/bin/bash
cd ..
cd ..
cd ..
../../bin/i18ndude rebuild-pot --pot genweb/rectorat/locales/genweb.rectorat.pot --create genweb.rectorat .
cd genweb/rectorat/locales/ca/LC_MESSAGES
../../../../../../../bin/i18ndude sync --pot ../../genweb.rectorat.pot genweb.rectorat.po
cd ..
cd ..
cd en
cd LC_MESSAGES
../../../../../../../bin/i18ndude sync --pot ../../genweb.rectorat.pot genweb.rectorat.po
cd ..
cd ..
cd es
cd LC_MESSAGES
../../../../../../../bin/i18ndude sync --pot ../../genweb.rectorat.pot genweb.rectorat.po
