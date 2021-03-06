Changelog
=========

1.20 (unreleased)
-----------------

- Nothing changed yet.


1.19 (2017-02-28)
-----------------

* added empty values if blank fields (strftime) [roberto.diaz]

1.18 (2016-12-15)
-----------------

* Refactor session ordering [Santi]
* Make time-less sessions sortable when Missing.Value [Santi]
* Make time-less sessions sortable [Santi]
* Sort sessions by datetime desc [Santi]

1.17 (2016-10-26)
-----------------

* Add type & frequency to indicators [Santi]
*  [Santi]
* - Add type and frequency to indicator definitions. [Santi]
* - Update indicators only when indicator updating is enabled, [Santi]
* i.e. when both service_id, ws_endpoint and ws_key are set. [Santi]

1.16 (2016-09-15)
-----------------

* Add indicators updating mechanism [Santiago Cortes]
*  [Santiago Cortes]
* - Define organ-n, arcord-n and sessio-n indicators. [Santiago Cortes]
* - Add IOrgangovern, IDocument and ISession 'removed event' and [Santiago Cortes]
* 'action succeded' updating subscribers. [Santiago Cortes]
* - Add control panel view with the indicators WS config params. [Santiago Cortes]
* - Add 'estatAprovacio' and 'dataSessio' indexes to catalog. [Santiago Cortes]

1.15 (2016-05-26)
-----------------

* added checks on send_message fields [roberto.diaz]
* added types to tiny for make relative links to rectorat objects [roberto.diaz]

1.14 (2016-04-07)
-----------------

* added finalhour to acta view [roberto.diaz]
* added horaFi to acta print [roberto.diaz]

1.13 (2016-03-17)
-----------------

* solved bug sending mail aq_parent [roberto.diaz]

1.12 (2016-03-15)
-----------------

* Merge branch 'master' of github.com:UPCnet/genweb.rectorat [roberto.diaz]
* TODO: added _unrestrictedGetObject() [roberto.diaz]

1.11 (2016-03-15)
-----------------



1.10 (2016-03-04)
-----------------



1.9 (2016-03-03)
----------------

* i18n: changing literals [roberto.diaz]

1.8 (2016-02-23)
----------------

* removed string [roberto.diaz]
* PEP8 [roberto.diaz]
* added div [root muntanyeta]
* i18n [roberto.diaz]
* mispelled error [root muntanyeta]
* last changes [roberto.diaz]
* added li i icon [roberto.diaz]
* removed li space [root muntanyeta]
* updated sendMessage [roberto.diaz]
* added cancel btn and interface to message view [root muntanyeta]
* added self to utils calls [roberto.diaz]
* changed isauthenticated to isEditor [roberto.diaz]
* remove rich_editor files [roberto.diaz]
* group utils functions [roberto.diaz]
* added senmessage view [roberto.diaz]
* changes [roberto.diaz]
* change tal:condition line [root muntanyeta]
* added UPC colors to table [root muntanyeta]
* Merge branch 'master' of github.com:UPCnet/genweb.rectorat [roberto.diaz]
* added new sorted table format [roberto.diaz]

1.7 (2016-02-11)
----------------

* editor can view button [roberto.diaz]
* removed Jquery dependencies [roberto.diaz]
* removed duplicated string [roberto.diaz]

1.6 (2016-02-02)
----------------

* Added local resources from richtext editor [roberto.diaz]
* customize js richtext icons [root muntanyeta]
* added collapse manually code [roberto.diaz]
* Merge branch 'master' of github.com:UPCnet/genweb.rectorat [roberto.diaz]
* testing js on mail [roberto.diaz]

1.5.3 (2016-01-26)
------------------

* changed string mails [roberto.diaz]
* added messages to mail [roberto.diaz]
* added accordion to ordre del dia [roberto.diaz]
* change membres to persones [roberto.diaz]
* normalize filename [roberto.diaz]
* add encode to filenames to avoid errors [Alberto Duran]

1.5.2 (2015-12-23)
------------------

* Merge branch 'master' of github.com:UPCnet/genweb.rectorat [roberto.diaz]
* hide urls in newsletters and remove 2 from url [roberto.diaz]
* removed bug in path [root muntanyeta]
* updated code [roberto.diaz]
* po changes [roberto.diaz]
* removed fixed path [roberto.diaz]
* added CSS [root muntanyeta]
* updated translations [roberto.diaz]
* added filename to indexer [roberto.diaz]
* added manager permission to view private files [roberto.diaz]
* added manager permission to view private files [roberto.diaz]
* added title to indexer [roberto.diaz]
* removed empty folder [roberto.diaz]
* changes December 2015 [roberto.diaz]
* superb changes [Roberto Diaz]
* remove check in doc view [roberto.diaz]
* changed ++genweb++ to ++gw++ [Roberto Diaz]
* i18n change [Roberto Diaz]

1.5.1 (2015-06-11)
------------------

* added permission to link [hanirok]

1.5 (2015-06-11)
----------------

* added missing translations print_view [Roberto Diaz]
* hide btn in print view, and order string in print [Roberto Diaz]
* new translation [Roberto Diaz]
* correct permission to link [Roberto Diaz]
* changed sender in mails [Roberto Diaz]
* mispelled strings [Roberto Diaz]
* error en po [Roberto Diaz]
* errors [Roberto Diaz]
* added correct translations & bugs [Roberto Diaz]
* added translations [Roberto Diaz]
* added try to send mail and fix anchor link [Roberto Diaz]
* added log to convocar sessio [Roberto Diaz]
* Added mail function to annotations [Roberto Diaz]
* added log table. TODO: username [Roberto Diaz]
* added annotations, next -> showing correctly! :) [Roberto Diaz]
* testing log [Roberto Diaz]
* added button send mail [Roberto Diaz]
* adding notifications history [Roberto Diaz]
* adding sendmail popup [Roberto Diaz]
* replaced from mail string in organ [Roberto Diaz]
* added informed state to documents [Roberto Diaz]

1.4 (2015-04-30)
----------------

* addapted templates to new accordion style (Marc) [Roberto Diaz]
* added indexer sort by sessionDate [Roberto Diaz]
* added accordion to members list [Roberto Diaz]
* last modified, first shown in sessions list [Roberto Diaz]
* solved error accents in mail fields [Roberto Diaz]
* swap docs public vs privats in session table [Roberto Diaz]

1.3 (2015-03-19)
----------------

* fixed searchableText to all DXT fields [Roberto Diaz]

1.2 (2015-03-19)
----------------

* aded widget to index [Roberto Diaz]
* Index multifile now is fully functional [Roberto Diaz]
* A medias: Tema custom indexer [Roberto Diaz]
* remove tal condition [Roberto Diaz]
* updated translations [Roberto Diaz]

1.1 (2015-03-09)
----------------

* renamed to public files [Roberto Diaz]
* changed string [Roberto Diaz]
* updated i18n workflow [Roberto Diaz]
* added br to mail message [Roberto Diaz]
* Merge branch 'master' of github.com:UPCnet/genweb.rectorat [Roberto Diaz]
* return obj ordered by positionInParent [Roberto Diaz]
* removed date from template [Roberto Diaz]
* changes in acta and session template [Roberto Diaz]
* added session to Folder [Roberto Diaz]
* added session to Folder [Roberto Diaz]
* added title to acta [Roberto Diaz]
* update print [Roberto Diaz]
* multiple templates changes [Roberto Diaz]
* modified date in acta print [Roberto Diaz]
* Merge branch 'master' of github.com:UPCnet/genweb.rectorat [Roberto Diaz]
* added acta footer [Roberto Diaz]
* passed empty fields [Roberto Diaz]
* added print view [Roberto Diaz]
* updated Organ to historic and templating... [Roberto Diaz]
* solved bug in mail + textindexer in acta + templates updated [Roberto Diaz]
* added jbot to override template for print.css in good order [Roberto Diaz]
* removed footer from print [Roberto Diaz]
* Organ: corrections on pt [Roberto Diaz]
* corrections on pt [Roberto Diaz]
* modified template [Roberto Diaz]
* first show public files in doc [Roberto Diaz]
* fixed path and i18n [Roberto Diaz]
* changing orde [Roberto Diaz]
* added state class [Roberto Diaz]
* changed listing table [Roberto Diaz]
* added acta [Roberto Diaz]
* renamod content and added CSS [Roberto Diaz]
* changes0 [Roberto Diaz]
* added referenceable and i18n in pt [Roberto Diaz]
* added richtext to some fields [Roberto Diaz]
* include package dexteritytextindexer dependency [Roberto Diaz]
* added dexterity translation custom fields not working in multifile... only text) [Roberto Diaz]
* modified css [Roberto Diaz]
* modified locale [Roberto Diaz]
* changed isAnon to isAuthent [Roberto Diaz]
* solved permissions on edit docs [Roberto Diaz]
* added checks to send mail [Roberto Diaz]
* print css: removed expanded links [Roberto Diaz]
* added addres to session & i18n & po [Roberto Diaz]
* modified visual content [Roberto Diaz]
* view state in edit mode [Roberto Diaz]
* changes to view PRINT.CSS [Roberto Diaz]
* check authenticated correctly [Roberto Diaz]
* added permissions to download multifile [Roberto Diaz]

1.0 (2015-01-08)
----------------

- Initial release
