from odoo import models, fields, api, _
import json
import os
import inspect


def registrant_file_path():
    dir_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return os.path.join(dir_path, 'registrant.json')


class ContactsList(models.Model):
    _name = 'contacts.list'

    name = fields.Char("Name")
    email = fields.Char("Email")
    phone = fields.Char("Phone")

    @api.multi
    def action_webinar_registration(self):
        """
        1) Try to match registrant's email to our Contacts list
        2) If not matched, try to match registrant's phone to our Contacts list
        3) Otherwise try to match our LeadsList with email (if Lead is matched, remove it from LeadsList and add to ContactsList)
        4) Else match our Leads with phone (same rule as above applies)
        5) If not matched, simply add it to ContactsList
        """

        f = open(registrant_file_path(), 'r')
        data = json.load(f)

        for registrant in data['registrant']:
            contacts = self.search([])
            leads = self.env['leads.list'].search([])

            matched_contact = contacts.filtered(
                lambda x: x.email == registrant['email'] or x.phone == registrant['phone'])
            matched_lead = leads.filtered(lambda x: x.email == registrant['email'])

            if matched_contact:
                matched_contact.write({
                    'name': registrant['name'] or matched_contact.name,
                    'email': registrant['email'] or matched_contact.email,
                    'phone': registrant['phone'] or matched_contact.phone
                })
            elif matched_lead:
                # remove it from leadslist
                matched_lead.write({
                    'name': registrant['name'] or matched_lead.name,
                    'email': registrant['email'] or matched_lead.email,
                    'phone': registrant['phone'] or matched_lead.phone
                })
                new_contact_record = {
                    'name': matched_lead['name'],
                    'email': matched_lead['email'],
                    'phone': matched_lead['phone']
                }
                # add to contact list
                self.create([new_contact_record])
                matched_lead.unlink()
            else:
                self.create([{
                    'name': registrant['name'],
                    'email': registrant['email'],
                    'phone': registrant['phone']
                }])

        f.close()

        # message_id = self.env['message.wizard'].create({'message': _("Successfully Imported.")})
        return {
            'name': _('Import Registrants'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            # pass the id
            'target': 'new'
        }
