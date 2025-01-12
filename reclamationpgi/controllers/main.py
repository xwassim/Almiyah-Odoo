# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64

class ReclamationController(http.Controller):

    # Route to render the web form
    @http.route('/reclamation_webform', type='http', auth='public', website=True)
    def reclamation_webform(self, **kw):
        return request.render('reclamationpgi.create_reclamation', {})

    # Route to handle form submission and create a Reclamation record
    @http.route('/create/reclamation', type='http', auth='public', website=True, csrf=False)
    def create_reclamation(self, **kw):
        try:
            # Create the Reclamant (Individual or Enterprise)
            reclamant_data = {
                'type': kw.get('type'),
                'reclamant_fname': kw.get('reclamant_fname'),
                'reclamant_lname': kw.get('reclamant_lname'),
                'reclamant_address': kw.get('reclamant_address'),
                'reclamant_city': kw.get('reclamant_city'),
                'reclamant_email': kw.get('reclamant_email'),
                'reclamant_phone': kw.get('reclamant_phone'),
            }

            # to see if the client wants to submit more than 1 file
            has_justification = bool(kw.get('has_justification'))

            if kw.get('type') == 'enterprise':
                reclamant_data.update({
                    'company_name': kw.get('company_name'),
                    'company_code': kw.get('company_code'),
                })

            # Create the Reclamant record
            reclamant = request.env['reclamationpgi.reclamant'].sudo().create(reclamant_data)

            # Find the partner with the name 'My Company'
            company_partner = request.env['res.partner'].search([('name', '=', 'My Company')], limit=1)

            # Handle file upload: get the PDF file from the form
            file = request.httprequest.files.get('justification_file')

            # Initialize the file content to None (in case no file is uploaded)
            file_content = None
            if file:
                # Read the file content as bytes
                file_content = file.read()

                # Encode the file content in base64
                file_content = base64.b64encode(file_content)
            
            #setup reclamation origin based on reclamant type
            temp = 'entreprise' if kw.get('type') == 'entreprise' else 'citoyen'
            
            # Create the Reclamation record and link it to the Reclamant
            request.env['reclamationpgi.reclamation'].sudo().create({
                'name': kw.get('name'),
                'date': kw.get('date'),
                'objet': kw.get('objet'),
                'description': kw.get('description'),
                'provenance': 'siteweb',
                'origin': temp,
                'agency_id': company_partner.id,
                'justification_file': file_content,  # Store the base64-encoded file content
                'reclamant_id': reclamant.id,
                'has_justification': has_justification,  # Store the checkbox value
            })

            # Render a thank-you page
            return request.render("reclamationpgi.reclamation_thanks", {})

        except Exception as e:
            # Log the error for debugging
            request.env['ir.logging'].create({
                'name': 'Reclamation Error',
                'type': 'server',
                'dbname': request.env.cr.dbname,
                'level': 'ERROR',
                'message': str(e),
                'path': 'reclamationpgi.controllers.main.create_reclamation',
                'func': 'create_reclamation',
                'line': 'Error in form submission and file handling',
            })

            # Show an error message to the user
            error_message = "Une erreur est apparue lors du traitement de votre demande"
            return request.render("reclamationpgi.reclamation_error", {'error_message': error_message})
