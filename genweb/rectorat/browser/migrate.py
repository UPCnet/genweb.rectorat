# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from datetime import datetime
from Products.CMFCore.utils import getToolByName
from plone import api
from plone.event.interfaces import IEventAccessor

import transaction


class migrateOrgans(BrowserView):

    def __call__(self):
        """ Adding send mail information to context in annotation format
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        # Default Carpeta Unitat
        name = 'Migrations'
        portal = api.portal.get()
        try:
            api.content.delete(portal['ca']['migrations'])
        except:
            None

        obj = api.content.create(
            id='migrations',
            title=name,
            type='genweb.organs.organsfolder',
            container=self.context)
        destination_folder = portal['ca']['migrations']

        items = portal_catalog.searchResults(
            portal_type=['genweb.rectorat.organgovern'],
        )

        # creating Organs de Govern inside Carpeta Unitat
        for item in items:
            obj = api.content.create(
                id=item.id,
                title=item.Title,
                type='genweb.organs.organgovern',
                container=destination_folder)
            old_item = item.getObject()
            obj.descripcioOrgan = old_item.descripcioOrgan.output
            obj.adrecaLlista = old_item.adrecaLlista
            obj.membresOrgan = old_item.membresOrgan.output
            obj.fromMail = old_item.fromMail
            obj.creators = old_item.creators
            obj.creation_date = old_item.creation_date
            transaction.commit()

            contained_items = old_item.items()
            cont = 0
            for value in contained_items:
                if value[1].portal_type == 'genweb.rectorat.sessio':
                    cont = cont + 1
                    old_session = value[1]
                    new_session = api.content.create(
                        id=old_session.id,
                        title=old_session.title,
                        type='genweb.organs.sessio',
                        container=obj)
                    new_session.numSessioShowOnly = str(cont).zfill(2)
                    new_session.numSessio = str(cont).zfill(2)
                    new_session.llocConvocatoria = old_session.llocConvocatoria

                    new_session.adrecaLlista = old_session.adrecaLlista
                    if old_session.membresConvocats:
                        new_session.membresConvocats = old_session.membresConvocats.output
                    if old_session.membresConvidats:
                        new_session.membresConvidats = old_session.membresConvidats.output
                    if old_session.llistaExcusats:
                        new_session.llistaExcusats = old_session.llistaExcusats.output
                    # ordredeldia
                    if old_session.bodyMail:
                        new_session.bodyMail = old_session.bodyMail.output
                    if old_session.signatura:
                        new_session.signatura = old_session.signatura.output
                    transaction.commit()

                    # Change start and end date
                    acc = IEventAccessor(new_session)
                    acc.start = datetime.combine(
                        old_session.dataSessio, old_session.horaInici)
                    acc.end = datetime.combine(
                        old_session.dataSessio, old_session.horaFi)
                    acc.timezone = 'Europe/Vienna'

                    transaction.commit()
                    # Acta inside session
                    old_actas = value[1].items()
                    for valueoldsactas in old_actas:
                        if valueoldsactas[1].portal_type == 'genweb.rectorat.acta':
                            # import ipdb;ipdb.set_trace()
                            old_acta = valueoldsactas[1]
                            new_acta = api.content.create(
                                id=old_acta.id,
                                title=old_acta.title,
                                type='genweb.organs.acta',
                                container=new_session)
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
                            if old_acta.ordreSessio:
                                newOrdenDelDia = old_acta.ordreSessio.output
                            if old_acta.actaBody:
                                newActaBody = old_acta.actaBody.output

                            new_acta.ordenDelDia = newOrdenDelDia + '</br/><hr/><br/>' + newActaBody
                            # enllacVideo
                            transaction.commit()

                            # Change start and end date
                            # acc = IEventAccessor(new_acta)
                            # acc.start = datetime.combine(
                            #     old_acta.dataSessio, old_acta.horaInici)
                            # acc.end = datetime.combine(
                            #     old_acta.dataSessio, old_acta.horaFi)
                            # acc.timezone = 'Europe/Vienna'

                if value[1].portal_type == 'genweb.rectorat.historicfolder':
                    old_historic_sessions = value[1].items()
                    for valueolds in old_historic_sessions:
                        if valueolds[1].portal_type == 'genweb.rectorat.sessio':
                            cont = cont + 1
                            old_session = valueolds[1]
                            new_session = api.content.create(
                                id=old_session.id,
                                title=old_session.title,
                                type='genweb.organs.sessio',
                                container=obj)
                            new_session.numSessioShowOnly = str(cont).zfill(2)
                            new_session.numSessio = str(cont).zfill(2)
                            # import ipdb;ipdb.set_trace()
                            new_session.llocConvocatoria = old_session.llocConvocatoria

                            new_session.adrecaLlista = old_session.adrecaLlista
                            if old_session.membresConvocats:
                                new_session.membresConvocats = old_session.membresConvocats.output
                            if old_session.membresConvidats:
                                new_session.membresConvidats = old_session.membresConvidats.output
                            if old_session.llistaExcusats:
                                new_session.llistaExcusats = old_session.llistaExcusats.output
                            # ordredeldia
                            if old_session.bodyMail:
                                new_session.bodyMail = old_session.bodyMail.output
                            if old_session.signatura:
                                new_session.signatura = old_session.signatura.output
                            transaction.commit()

                            # Change start and end date
                            acc = IEventAccessor(new_session)
                            acc.start = datetime.combine(
                                old_session.dataSessio, old_session.horaInici)
                            acc.end = datetime.combine(
                                old_session.dataSessio, old_session.horaFi)
                            acc.timezone = 'Europe/Vienna'
        return 'OK'
