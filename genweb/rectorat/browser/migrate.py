# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from datetime import datetime
from Products.CMFCore.utils import getToolByName
from plone import api
from plone.event.interfaces import IEventAccessor
from plone.namedfile.file import NamedBlobFile
import transaction
from zope.annotation.interfaces import IAnnotations
from operator import itemgetter
import logging
import re

filename = 'import.log'  # local
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=filename,
                    level=logging.DEBUG)


def pp(message, item, f="None"):
    """Function to show messages in file and screen """
    if f is "None":
        f = open(filename, 'a')
    if item is not None:
        print " ## " + str(message) + " @@ " + str(item)
        f.write(" ## " + str(message) + " @@ " + str(item) + "\n")
    if message is "Close":
        f.close()


class migrateOrgans(BrowserView):

    def __call__(self):
        """ Migrate Organs from v1.0 to v2.0 """
        date = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        pp('-------------------------------', '')
        pp("START migration proces", date)
        portal_catalog = getToolByName(self, 'portal_catalog')
        # Default Carpeta Unitat
        name = 'Migrations'
        portal = api.portal.get()

        try:
            api.content.delete(portal['ca']['migrations'])
        except:
            None

        api.content.create(
            id='migrations',
            title=name,
            type='genweb.organs.organsfolder',
            safe_id=True,
            container=self.context)
        destination_folder = portal['ca']['migrations']

        items = portal_catalog.searchResults(
            portal_type=['genweb.rectorat.organgovern'],
        )
        pp("Items to migrate", len(items))

        # creating Organs de Govern in Carpeta Unitat
        for item in items:
            new_organ = api.content.create(
                title=item.Title,
                type='genweb.organs.organgovern',
                container=destination_folder,
                safe_id=True,)
            pp("Migrating", item.Title)

            old_organ = item.getObject()
            if old_organ.descripcioOrgan:
                new_organ.descripcioOrgan = old_organ.descripcioOrgan.output
            new_organ.adrecaLlista = old_organ.adrecaLlista
            if old_organ.membresOrgan:
                new_organ.membresOrgan = old_organ.membresOrgan.output
            new_organ.fromMail = old_organ.fromMail
            new_organ.creators = old_organ.creators
            new_organ.modification_date = old_organ.modification_date
            transaction.commit()
            pp("Created OG", str(item.getPath()) + " > " + str(new_organ.absolute_url_path()))

            contained_items = old_organ.items()
            contSession = 0
            for value in contained_items:
                old_session = value[1]
                if value[1].portal_type == 'genweb.rectorat.sessio':
                    contSession = contSession + 1
                    new_session = api.content.create(
                        id=old_session.id,
                        title=old_session.title,
                        type='genweb.organs.sessio',
                        container=new_organ,
                        safe_id=True,)
                    new_session.numSessioShowOnly = str(contSession).zfill(2)
                    new_session.numSessio = str(contSession).zfill(2)
                    new_session.llocConvocatoria = old_session.llocConvocatoria
                    new_session.adrecaLlista = old_session.adrecaLlista
                    if old_session.membresConvocats:
                        new_session.membresConvocats = old_session.membresConvocats.output
                    if old_session.membresConvidats:
                        new_session.membresConvidats = old_session.membresConvidats.output
                    if old_session.llistaExcusats:
                        new_session.llistaExcusats = old_session.llistaExcusats.output
                    if old_session.bodyMail:
                        new_session.bodyMail = old_session.bodyMail.output
                    if old_session.signatura:
                        new_session.signatura = old_session.signatura.output
                    # Change start and end date
                    acc = IEventAccessor(new_session)
                    acc.start = datetime.combine(
                        old_session.dataSessio, old_session.horaInici)
                    acc.end = datetime.combine(
                        old_session.dataSessio, old_session.horaFi)
                    acc.timezone = 'Europe/Madrid'
                    new_session.migrated = True
                    new_session.reindexObject()
                    transaction.commit()
                    old_state = api.content.get_state(obj=old_session)
                    # old_state == 'preparing' default is the same don't do nothing
                    if old_state == 'convocat':
                        api.content.transition(obj=new_session, transition='convocar')
                    if old_state == 'closed':
                        api.content.transition(obj=new_session, transition='convocar')
                        api.content.transition(obj=new_session, transition='realitzar')
                        api.content.transition(obj=new_session, transition='tancar')
                    pp("Created SESSION", str(old_session.absolute_url_path()) + " > " + str(new_session.absolute_url_path()))
                    try:
                        old_annotations = IAnnotations(old_session)['genweb.rectorat.logMail']
                        data = []
                        index = 0
                        for item in old_annotations:
                            values = dict(index=index + 1,
                                          dateMail=item['dateMail'].strftime('%d/%m/%Y %H:%M:%S'),
                                          message=item['fromMail'].split(':')[0],
                                          fromMail=item['fromMail'].split(':')[1],
                                          toMail=item['toMail'])
                            data.append(values)
                            index = index + 1
                        IAnnotations(new_session)['genweb.organs.logMail'] = data
                    except:
                        pp("SESSION without log entries", old_session.absolute_url_path())
                        continue
                    old_documents = old_session.items()
                    results = []
                    for item in old_documents:
                        if hasattr(item[1], 'proposalPoint'):
                            numeroProposal = item[1].proposalPoint
                            # Check .- en el num de punto para borrarlo...
                            try:
                                if '-' in numeroProposal or '.' in numeroProposal:
                                    if numeroProposal[-1] == '-':
                                        if numeroProposal[-2] == '.':
                                            numeroProposal = numeroProposal[:-2]
                                        else:
                                            numeroProposal = numeroProposal[:-1]
                                    if numeroProposal[-1] == '.':
                                        numeroProposal = numeroProposal[:-1]
                            except:
                                # En un acta de ESEIAAT no tienen número
                                numeroProposal = 1

                            results.append(dict(index=numeroProposal, object=item[1]))
                    docsByIndex = sorted(results, key=itemgetter('index'))

                    # Import ordre del dia as punt 00
                    ordreDelDia = api.content.create(
                        id='ordre-del-dia',
                        title="Ordre del dia",
                        type='genweb.organs.punt',
                        container=new_session,
                        safe_id=True)
                    ordreDelDia.proposalPoint = '00'
                    ordreDelDia.estatsLlista = 'Aprovat'
                    if old_session.ordreSessio:
                        ordreDelDia.defaultContent = old_session.ordreSessio.output
                    ordreDelDia.creators = old_session.creators
                    ordreDelDia.modification_date = old_session.modification_date

                    for valueoldsdocs in docsByIndex:
                        # Iniciem creacio dels documents en punts/subpunts/acords
                        puntsessio = valueoldsdocs['object']
                        if puntsessio.portal_type != 'genweb.rectorat.acta':
                            if '.' in puntsessio.proposalPoint:
                                puntId = puntsessio.proposalPoint.split('.')[0]
                                existeix = False
                                for ids in new_session.items():
                                    if ids[1].proposalPoint == puntId:
                                        existeix = True

                                if not existeix:
                                    # Si no existe lo creo como Esborrany
                                    createdSubPunt = api.content.create(
                                        title=puntId,
                                        type='genweb.organs.punt',
                                        container=new_session,
                                        safe_id=True)
                                    createdSubPunt.proposalPoint = puntId
                                    createdSubPunt.estatsLlista = 'Aprovat'
                                    createdSubPunt.creators = old_session.creators
                                    createdSubPunt.modification_date = old_session.modification_date

                                    if puntsessio.agreement:
                                        # En un acord
                                        new_acord = api.content.create(
                                            id=puntsessio.id,
                                            title=puntsessio.title,
                                            type='genweb.organs.acord',
                                            container=createdSubPunt,
                                            safe_id=True)
                                        new_acord.proposalPoint = puntsessio.proposalPoint
                                        new_acord.agreement = puntsessio.agreement
                                        estat = puntsessio.estatAprovacio
                                        if estat == 'Draft':
                                            new_acord.estatsLlista = 'Esborrany'
                                        if estat == 'Informed':
                                            new_acord.estatsLlista = 'Informat'
                                        if estat == 'Approved':
                                            new_acord.estatsLlista = 'Aprovat'
                                        if estat == 'Rejected':
                                            new_acord.estatsLlista = 'No aprovat'
                                        if estat == 'Pending':
                                            new_acord.estatsLlista = 'Derogat'

                                        if puntsessio.PublishedFiles:
                                            for file in puntsessio.PublishedFiles:
                                                public_file = NamedBlobFile(
                                                    data=file.data,
                                                    contentType=file.contentType,
                                                    filename=file.filename
                                                )
                                                new_file = api.content.create(
                                                    id=file.filename,
                                                    title=file.filename,
                                                    type='genweb.organs.file',
                                                    container=new_acord,
                                                    safe_id=True,)
                                                new_file.visiblefile = public_file

                                        if puntsessio.OriginalFiles:
                                            pp("WARNING: Check files manually ", puntsessio.absolute_url_path())
                                            for file in puntsessio.OriginalFiles:
                                                reserved_file = NamedBlobFile(
                                                    data=file.data,
                                                    contentType=file.contentType,
                                                    filename=file.filename
                                                )
                                                new_file = api.content.create(
                                                    id=file.filename,
                                                    title=file.filename,
                                                    type='genweb.organs.file',
                                                    container=new_acord,
                                                    safe_id=True,)
                                                new_file.hiddenfile = reserved_file

                                    else:
                                        # es un punt
                                        new_punt = api.content.create(
                                            id=puntsessio.id,
                                            title=puntsessio.title,
                                            type='genweb.organs.subpunt',
                                            container=createdSubPunt,
                                            safe_id=True)
                                        new_punt.proposalPoint = puntsessio.proposalPoint
                                        estat = puntsessio.estatAprovacio

                                        if estat == 'Draft':
                                            new_punt.estatsLlista = 'Esborrany'
                                        if estat == 'Informed':
                                            new_punt.estatsLlista = 'Informat'
                                        if estat == 'Approved':
                                            new_punt.estatsLlista = 'Aprovat'
                                        if estat == 'Rejected':
                                            new_punt.estatsLlista = 'No aprovat'
                                        if estat == 'Pending':
                                            new_punt.estatsLlista = 'Derogat'

                                        if puntsessio.PublishedFiles:
                                            for file in puntsessio.PublishedFiles:
                                                public_file = NamedBlobFile(
                                                    data=file.data,
                                                    contentType=file.contentType,
                                                    filename=file.filename
                                                )
                                                new_file = api.content.create(
                                                    id=file.filename,
                                                    title=file.filename,
                                                    type='genweb.organs.file',
                                                    container=new_punt,
                                                    safe_id=True,)
                                                new_file.visiblefile = public_file

                                        if puntsessio.OriginalFiles:
                                            pp("WARNING: Check files manually ", puntsessio.absolute_url_path())
                                            for file in puntsessio.OriginalFiles:
                                                reserved_file = NamedBlobFile(
                                                    data=file.data,
                                                    contentType=file.contentType,
                                                    filename=file.filename
                                                )
                                                new_file = api.content.create(
                                                    id=file.filename,
                                                    title=file.filename,
                                                    type='genweb.organs.file',
                                                    container=new_punt,
                                                    safe_id=True,)
                                                new_file.hiddenfile = reserved_file
                                else:
                                    # print " ### El punt existeix"
                                    for objecte in new_session.items():
                                        if objecte[1].proposalPoint == puntId:
                                            folderObject = objecte[1]

                                    if puntsessio.agreement:
                                        # En un acord
                                        try:
                                            new_acord = api.content.create(
                                                id=puntsessio.id,
                                                title=puntsessio.title,
                                                type='genweb.organs.acord',
                                                container=folderObject,
                                                safe_id=True)
                                        except:
                                            pp("proposalpoint con id raro", puntsessio.absolute_url_path())
                                            new_acord = api.content.create(
                                                id=puntsessio.id,
                                                title=puntsessio.title,
                                                type='genweb.organs.acord',
                                                container=new_session,
                                                safe_id=True)

                                        new_acord.proposalPoint = puntsessio.proposalPoint
                                        new_acord.agreement = puntsessio.agreement
                                        new_acord.creators = puntsessio.creators
                                        new_acord.modification_date = puntsessio.modification_date

                                        estat = puntsessio.estatAprovacio
                                        if estat == 'Draft':
                                            new_acord.estatsLlista = 'Esborrany'
                                        if estat == 'Informed':
                                            new_acord.estatsLlista = 'Informat'
                                        if estat == 'Approved':
                                            new_acord.estatsLlista = 'Aprovat'
                                        if estat == 'Rejected':
                                            new_acord.estatsLlista = 'No aprovat'
                                        if estat == 'Pending':
                                            new_acord.estatsLlista = 'Derogat'

                                        if puntsessio.PublishedFiles:
                                            for file in puntsessio.PublishedFiles:
                                                public_file = NamedBlobFile(
                                                    data=file.data,
                                                    contentType=file.contentType,
                                                    filename=file.filename
                                                )
                                                new_file = api.content.create(
                                                    id=file.filename,
                                                    title=file.filename,
                                                    type='genweb.organs.file',
                                                    container=new_acord,
                                                    safe_id=True,)
                                                new_file.visiblefile = public_file

                                        if puntsessio.OriginalFiles:
                                            for file in puntsessio.OriginalFiles:
                                                reserved_file = NamedBlobFile(
                                                    data=file.data,
                                                    contentType=file.contentType,
                                                    filename=file.filename
                                                )
                                                new_file = api.content.create(
                                                    id=file.filename,
                                                    title=file.filename,
                                                    type='genweb.organs.file',
                                                    container=new_acord,
                                                    safe_id=True,)
                                                new_file.hiddenfile = reserved_file

                                    else:
                                        # es un punt
                                        try:
                                            new_punt = api.content.create(
                                                id=puntsessio.id,
                                                title=puntsessio.title,
                                                type='genweb.organs.subpunt',
                                                container=folderObject,
                                                safe_id=True)
                                        except:
                                            try:
                                                new_punt = api.content.create(
                                                    id=puntsessio.id,
                                                    title=puntsessio.title,
                                                    type='genweb.organs.subpunt',
                                                    container=folderObject.aq_parent,
                                                    safe_id=True)
                                            except:
                                                new_punt = api.content.create(
                                                    id=puntsessio.id,
                                                    title=puntsessio.title,
                                                    type='genweb.organs.punt',
                                                    container=folderObject.aq_parent,
                                                    safe_id=True)
                                        new_punt.proposalPoint = puntsessio.proposalPoint
                                        new_punt.creators = puntsessio.creators
                                        new_punt.modification_date = puntsessio.modification_date

                                        estat = puntsessio.estatAprovacio
                                        if estat == 'Draft':
                                            new_punt.estatsLlista = 'Esborrany'
                                        if estat == 'Informed':
                                            new_punt.estatsLlista = 'Informat'
                                        if estat == 'Approved':
                                            new_punt.estatsLlista = 'Aprovat'
                                        if estat == 'Rejected':
                                            new_punt.estatsLlista = 'No aprovat'
                                        if estat == 'Pending':
                                            new_punt.estatsLlista = 'Derogat'

                                        if puntsessio.PublishedFiles:
                                            for file in puntsessio.PublishedFiles:
                                                public_file = NamedBlobFile(
                                                    data=file.data,
                                                    contentType=file.contentType,
                                                    filename=file.filename
                                                )
                                                new_file = api.content.create(
                                                    id=file.filename,
                                                    title=file.filename,
                                                    type='genweb.organs.file',
                                                    container=new_punt,
                                                    safe_id=True,)
                                                new_file.visiblefile = public_file

                                        if puntsessio.OriginalFiles:
                                            for file in puntsessio.OriginalFiles:
                                                reserved_file = NamedBlobFile(
                                                    data=file.data,
                                                    contentType=file.contentType,
                                                    filename=file.filename
                                                )
                                                new_file = api.content.create(
                                                    id=file.filename,
                                                    title=file.filename,
                                                    type='genweb.organs.file',
                                                    container=new_punt,
                                                    safe_id=True,)
                                                new_file.hiddenfile = reserved_file

                            else:
                                if puntsessio.portal_type == 'genweb.rectorat.document':
                                    if puntsessio.agreement:
                                        # En un acord
                                        new_acord = api.content.create(
                                            id=puntsessio.id,
                                            title=puntsessio.title,
                                            type='genweb.organs.acord',
                                            container=new_session,
                                            safe_id=True)
                                        new_acord.proposalPoint = puntsessio.proposalPoint
                                        new_acord.agreement = puntsessio.agreement
                                        new_acord.creators = puntsessio.creators
                                        new_acord.modification_date = puntsessio.modification_date
                                        estat = puntsessio.estatAprovacio

                                        if estat == 'Draft':
                                            new_acord.estatsLlista = 'Esborrany'
                                        if estat == 'Informed':
                                            new_acord.estatsLlista = 'Informat'
                                        if estat == 'Approved':
                                            new_acord.estatsLlista = 'Aprovat'
                                        if estat == 'Rejected':
                                            new_acord.estatsLlista = 'No aprovat'
                                        if estat == 'Pending':
                                            new_acord.estatsLlista = 'Derogat'

                                    else:
                                        # es un punt
                                        new_punt = api.content.create(
                                            id=puntsessio.id,
                                            title=puntsessio.title,
                                            type='genweb.organs.punt',
                                            container=new_session,
                                            safe_id=True)
                                        new_punt.proposalPoint = puntsessio.proposalPoint
                                        new_punt.creators = puntsessio.creators
                                        new_punt.modification_date = puntsessio.modification_date

                                        estat = puntsessio.estatAprovacio

                                        if estat == 'Draft':
                                            new_punt.estatsLlista = 'Esborrany'
                                        if estat == 'Informed':
                                            new_punt.estatsLlista = 'Informat'
                                        if estat == 'Approved':
                                            new_punt.estatsLlista = 'Aprovat'
                                        if estat == 'Rejected':
                                            new_punt.estatsLlista = 'No aprovat'
                                        if estat == 'Pending':
                                            new_punt.estatsLlista = 'Derogat'

                                    if puntsessio.PublishedFiles:
                                        for file in puntsessio.PublishedFiles:
                                            public_file = NamedBlobFile(
                                                data=file.data,
                                                contentType=file.contentType,
                                                filename=file.filename
                                            )
                                            new_file = api.content.create(
                                                id=file.filename,
                                                title=file.filename,
                                                type='genweb.organs.file',
                                                container=new_punt,
                                                safe_id=True,)
                                            new_file.visiblefile = public_file

                                    if puntsessio.OriginalFiles:
                                        for file in puntsessio.OriginalFiles:
                                            reserved_file = NamedBlobFile(
                                                data=file.data,
                                                contentType=file.contentType,
                                                filename=file.filename
                                            )
                                            new_file = api.content.create(
                                                id=file.filename,
                                                title=file.filename,
                                                type='genweb.organs.file',
                                                container=new_punt,
                                                safe_id=True,)
                                            new_file.hiddenfile = reserved_file

                    # Acta inside session
                    old_actas = old_session.items()
                    for valueoldsactas in old_actas:
                        if valueoldsactas[1].portal_type == 'genweb.rectorat.acta':
                            old_acta = valueoldsactas[1]
                            new_acta = api.content.create(
                                id=old_acta.id,
                                title=old_acta.title,
                                type='genweb.organs.acta',
                                container=new_session,
                                safe_id=True)
                            new_acta.llocConvocatoria = old_acta.llocConvocatoria

                            if old_acta.membresConvocats:
                                new_acta.membresConvocats = old_acta.membresConvocats.output
                            if old_acta.membresConvidats:
                                new_acta.membresConvidats = old_acta.membresConvidats.output
                            if old_acta.llistaExcusats:
                                new_acta.llistaExcusats = old_acta.llistaExcusats.output
                            if old_acta.llistaNoAssistens:
                                new_acta.llistaNoAssistens = old_acta.llistaNoAssistens.output
                            # ordredeldia
                            newOrdenDelDia = newActaBody = footer = ''
                            if old_acta.ordreSessio:
                                newOrdenDelDia = "<hr/><h4>Ordre del dia</h4><hr/>" + old_acta.ordreSessio.output
                            if old_acta.actaBody:
                                newActaBody = "<hr/><h4>Acta</h4><hr/>" + old_acta.actaBody.output
                            if old_acta.footer:
                                footer = "<hr/><h4>Peu del Acta</h4><hr/>" + old_acta.footer.output
                            new_acta.ordenDelDia = newOrdenDelDia + newActaBody + footer
                            # enllacVideo
                            new_acta.horaInici = datetime.combine(
                                old_acta.dataSessio, old_acta.horaInici)
                            new_acta.horaFi = datetime.combine(
                                old_acta.dataSessio, old_acta.horaFi)
                            new_acta.reindexObject()
                            transaction.commit()
                            pp("Created ACTA", str(old_acta.absolute_url_path()) + " > " + str(new_acta.absolute_url_path()))

                            if old_acta.OriginalFiles:
                                file = old_acta.OriginalFiles[0]
                                reserved_file = NamedBlobFile(
                                    data=file.data,
                                    contentType=file.contentType,
                                    filename=file.filename
                                )
                                new_acta.file = reserved_file

                            if old_acta.footer:
                                hrefs = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', old_acta.footer.output)
                                for audio in hrefs:
                                    if '.mp3' in audio:
                                        print " ## This Acta has an Audio..."
                                        filename_path = '/' + '/'.join(str(audio).split('/')[3:])
                                        old_file = api.content.find(path=filename_path)[0]
                                        blob_file = old_file.getObject()
                                        mp3_file = NamedBlobFile(
                                            data=blob_file.file.data,
                                            contentType=blob_file.file.contentType,
                                            filename=blob_file.file.filename
                                        )
                                        new_file = api.content.create(
                                            id=old_file.id,
                                            title=old_file.Title,
                                            type='genweb.organs.audio',
                                            container=new_acta,
                                            safe_id=True,)
                                        new_file.file = mp3_file
                                        transaction.commit()
                                        pp("Created AUDIO in Acta", str(audio) + " > " + str(new_acta.absolute_url_path()))

                # if value[1].portal_type == 'genweb.rectorat.historicfolder':
                #     old_historic_sessions = value[1].items()
                #     for valueolds in old_historic_sessions:
                #         if valueolds[1].portal_type == 'genweb.rectorat.sessio':
                #             cont = cont + 1
                #             old_hist_session = valueolds[1]
                #             new_hist_session = api.content.create(
                #                 id=old_hist_session.id,
                #                 title=old_hist_session.title,
                #                 type='genweb.organs.sessio',
                #                 container=new_organ,
                #                 safe_id=True,)
                #             new_hist_session.numSessioShowOnly = str(cont).zfill(2)
                #             new_hist_session.numSessio = str(cont).zfill(2)
                #             new_hist_session.llocConvocatoria = old_hist_session.llocConvocatoria
                #             new_hist_session.adrecaLlista = old_hist_session.adrecaLlista
                #             if old_hist_session.membresConvocats:
                #                 new_hist_session.membresConvocats = old_hist_session.membresConvocats.output
                #             if old_hist_session.membresConvidats:
                #                 new_hist_session.membresConvidats = old_hist_session.membresConvidats.output
                #             if old_hist_session.llistaExcusats:
                #                 new_hist_session.llistaExcusats = old_hist_session.llistaExcusats.output
                #             if old_hist_session.bodyMail:
                #                 new_hist_session.bodyMail = old_hist_session.bodyMail.output
                #             if old_hist_session.signatura:
                #                 new_hist_session.signatura = old_hist_session.signatura.output
                #             acc = IEventAccessor(new_hist_session)
                #             acc.start = datetime.combine(
                #                 old_hist_session.dataSessio, old_hist_session.horaInici)
                #             acc.end = datetime.combine(
                #                 old_hist_session.dataSessio, old_hist_session.horaFi)
                #             acc.timezone = 'Europe/Madrid'
                #             new_hist_session.reindexObject()
                #             new_hist_session.migrated = True
                #             transaction.commit()
                #             old_state = api.content.get_state(obj=old_hist_session)
                #             # old_state == 'preparing' default is the same don't do nothing
                #             if old_state == 'convocat':
                #                 api.content.transition(obj=new_hist_session, transition='convocar')
                #             if old_state == 'closed':
                #                 api.content.transition(obj=new_hist_session, transition='convocar')
                #                 api.content.transition(obj=new_hist_session, transition='realitzar')
                #                 api.content.transition(obj=new_hist_session, transition='tancar')

                #             pp("Created HISTORIC SESSION", str(old_hist_session.absolute_url_path()) + " > " + str(new_hist_session.absolute_url_path()))

                #             old_hist_actas = valueolds[1].items()
                #             for valueoldsHistActas in old_hist_actas:
                #                 if valueoldsHistActas[1].portal_type == 'genweb.rectorat.acta':
                #                     old_hist_acta = valueoldsHistActas[1]
                #                     new_hist_acta = api.content.create(
                #                         id=old_hist_acta.id,
                #                         title=old_hist_acta.title,
                #                         type='genweb.organs.acta',
                #                         safe_id=True,
                #                         container=new_hist_session)
                #                     pp("Created HISTORIC ACTA", str(old_hist_acta.absolute_url_path()) + " > " + str(new_hist_acta.absolute_url_path()))

                #                     new_hist_acta.llocConvocatoria = old_hist_acta.llocConvocatoria
                #                     if old_hist_acta.membresConvocats:
                #                         new_hist_acta.membresConvocats = old_hist_acta.membresConvocats.output
                #                     if old_hist_acta.membresConvidats:
                #                         new_hist_acta.membresConvidats = old_hist_acta.membresConvidats.output
                #                     if old_hist_acta.llistaExcusats:
                #                         new_hist_acta.llistaExcusats = old_hist_acta.llistaExcusats.output
                #                     if old_hist_acta.llistaNoAssistens:
                #                         new_hist_acta.llistaNoAssistens = old_hist_acta.llistaNoAssistens.output
                #                     # ordredeldia
                #                     newOrdenDelDia = newActaBody = footer = ''
                #                     if old_hist_acta.ordreSessio:
                #                         newOrdenDelDia = '<hr/><h4>Ordre del dia</h4><hr/>' + old_hist_acta.ordreSessio.output
                #                     if old_hist_acta.actaBody:
                #                         newActaBody = '<hr/><h4>Acta</h4><hr/>' + old_hist_acta.actaBody.output
                #                     if old_hist_acta.footer:
                #                         footer = "<hr/><h4>Peu del Acta</h4><hr/>" + old_hist_acta.footer.output
                #                     new_hist_acta.ordenDelDia = newOrdenDelDia + newActaBody + footer
                #                     # enllacVideo
                #                     new_hist_acta.horaInici = datetime.combine(
                #                         old_hist_acta.dataSessio, old_hist_acta.horaInici)
                #                     new_hist_acta.horaFi = datetime.combine(
                #                         old_hist_acta.dataSessio, old_hist_acta.horaFi)
                #                     transaction.commit()

                #                     if old_hist_acta.footer:
                #                         hrefs = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', old_hist_acta.footer.output)
                #                         for audio in hrefs:
                #                             if '.mp3' in audio:
                #                                 pp("Adding AUDIO to this HISTORIC ACTA", str(old_hist_acta.absolute_url_path()) + ' > ' + str(audio))
                #                                 filename_path = '/' + '/'.join(str(audio).split('/')[3:])
                #                                 old_file = api.content.find(path=filename_path)[0]
                #                                 blob_file = old_file.getObject()
                #                                 mp3_file = NamedBlobFile(
                #                                     data=blob_file.file.data,
                #                                     contentType=blob_file.file.contentType,
                #                                     filename=blob_file.file.filename
                #                                 )
                #                                 new_file = api.content.create(
                #                                     id=old_file.id,
                #                                     title=old_file.Title,
                #                                     type='genweb.organs.audio',
                #                                     container=new_hist_acta,
                #                                     safe_id=True,)
                #                                 new_file.file = mp3_file
                #                                 transaction.commit()
                #                                 pp("Created AUDIO IN HISTORIC ACTA", old_hist_acta.absolute_url_path())

        date = datetime.now().strftime("%Y%m%d-%H:%M:%S")

        pp("END migration proces", date)
        pp('-------------------------------', '')
        pp("Close", None)

        result = []
        with open(filename) as f:
            line = f.read().replace('\n', '<br/>')
            result.append(line)

        return result[0]
