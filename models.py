from odoo import models, fields , api 

class Reclamation(models.Model):
    _name = 'reclamationpgi.reclamation'
    _description = "Gestion des réclamations"

    # Informations générales
    name = fields.Char(string="Nom", required=True)
    date = fields.Date(string="Date de la Réclamation", required=True)
    objet = fields.Char(string="Objet de la Réclamation", required=True)
    description = fields.Text(string="Description de la Réclamation", required=True)
    justification_file = fields.Binary(string="Pièces Justificatives")
    #to check if the client want to submit more than one file
    has_justification = fields.Boolean(string="A-t-il d'autres pièces justificatives ?", default=False)
    # Agence
    agency_id = fields.Many2one('res.partner', string="Agence", required=False, help="Agence associée à la réclamation")

    # Origine de la réclamation
    origin = fields.Selection([
        ('citoyen', 'Citoyen'),
        ('entreprise', 'Entreprise'),
        ('cellule_veille', 'Cellule de Veille')
    ], string="Origine de la Réclamation", required=False)

    #provenance de la réclamation
    provenance = fields.Selection([
         ('siteweb','Formulaire du SiteWeb'),
         ('telephone','Appel Téléphone'),
         ('presentiel','Présentiel'),
    ], string="Provenance de la réclamation",required = True)

    # Informations sur le réclamant
    reclamant_id = fields.Many2one('reclamationpgi.reclamant', string="Réclamant")

    # Assignation de l'agent
    assigned_agent = fields.Many2one('hr.employee', string="Agent Assigné")

    # Statut de la réclamation
    status = fields.Selection([
        ('pending', 'En Attente'),
        ('processed', 'Traitée'),
        ('archived', 'Archivée')
    ], string="Statut", default='pending',required=False)

    # Priorité et complexité
    urgency = fields.Boolean(string="Urgence", default=False, help="Indique si la réclamation est urgente.",required=False)
    claim_type = fields.Selection([
        ('commercial', 'Commerciale'),
        ('technical', 'Technique')
    ], string="Type de Réclamation",required=False)
    complexity = fields.Selection([
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Élevée')
    ], string="Complexité",required=False)
    severity = fields.Selection([
        ('minor', 'Mineure'),
        ('major', 'Majeure'),
        ('critical', 'Critique')
    ], string="Gravité",required=False)

class Agent(models.Model):
        _inherit = 'hr.employee'

     # Champs spécifiques pour un agent
        agency_id = fields.Many2one('res.partner', string="Agence", help="Agence associée à l'agent.")
        role = fields.Selection([
            ('agent_simple', 'Agent Simple'),
            ('chef_equipe_technique', 'Chef d’Équipe Technique'),
            ('chef_equipe_commercial', 'Chef d’Équipe Commercial'),
            ('agent_technique', 'Agent Technique'),
            ('agent_commission_redressement', 'Agent Commission Redressement'),
            ('responsable_agence', 'Responsable Agence')
        ], string="Rôle", required=True, help="Rôle de l'agent dans l'organisation.")
        
        department = fields.Selection([
        ('commercial', 'Commerciale'),
        ('technical', 'Technique')
    ], string="Departement agent")

class Reclamant(models.Model):
    _name = 'reclamationpgi.reclamant'
    _description = "Informations sur le Réclamant"

    type = fields.Selection([
        ('individual', 'Individu'),
        ('enterprise', 'Entreprise')
    ], string="Type de Réclamant", required=True)

    # Fields for Individuals
    reclamant_fname = fields.Char(string="Prénom", states={'readonly': [('type', '!=', 'individual')]})
    reclamant_lname = fields.Char(string="Nom", states={'readonly': [('type', '!=', 'individual')]})
    reclamant_address = fields.Text(string="Adresse", states={'readonly': [('type', '!=', 'individual')]})
    reclamant_city = fields.Char(string="Commune", states={'readonly': [('type', '!=', 'individual')]})
    #added by wassim 
    reclamant_email = fields.Char(string="Email du reclamant", states={'readonly': [('type', '!=', 'individual')]})
    reclamant_phone = fields.Char(string="Telephone du reclamant", states={'readonly': [('type', '!=', 'individual')]})

    # Fields for Enterprises
    company_name = fields.Char(string="Nom de l'Entreprise", states={'readonly': [('type', '!=', 'enterprise')]})
    company_address = fields.Text(string="Adresse de l'Entreprise", states={'readonly': [('type', '!=', 'enterprise')]})
    company_phone = fields.Char(string="Téléphone de l'Entreprise", states={'readonly': [('type', '!=', 'enterprise')]})
    company_email = fields.Char(string="Email de l'Entreprise", states={'readonly': [('type', '!=', 'enterprise')]})
    company_sector = fields.Char(string="Secteur d'Activité", states={'readonly': [('type', '!=', 'enterprise')]})
    # added by wassim (champ raison social)
    company_code = fields.Char(string="Raison social",states={'readonly': [('type', '!=', 'enterprise')]})
    
    survey_id = fields.Many2one('survey.survey', string="Survey")


class Equipe(models.Model):
    _name = 'reclamationpgi.equipe'
    _description = 'Équipe'

    name = fields.Char(string="Nom de l'Équipe", required=True)
    members_ids = fields.Many2many('hr.employee', string="Membres de l'Équipe")
    chef_id = fields.Many2one('hr.employee', string="Chef d’Équipe", required=True)
    reclamations_ids = fields.Many2many('reclamationpgi.reclamation', string="Réclamations Assignées")
    
class Intervention(models.Model):
    _name = 'reclamationpgi.intervention'
    _description = 'Intervention'

    name = fields.Char(string="Nom de l'Intervention", required=True)
    reclamation_id = fields.Many2one('reclamationpgi.reclamation', string="Réclamation")
    equipe_id = fields.Many2one('reclamationpgi.equipe', string="Équipe Assignée")
    statut = fields.Selection([
        ('pas_commence', 'Pas Commencée'),
        ('en_cours', 'En Cours'),
        ('cloturee', 'Clôturée')
    ], string="Statut", default='pas_commence')
    date = fields.Date(string="Date de l'Intervention")

    # Pour les interventions techniques
    actions_realisees = fields.Text(string="Actions Réalisées")
    deplacements_ids = fields.Many2many('reclamationpgi.deplacement', string="Déplacements")

    # Pour les interventions commerciales
    objet = fields.Text(string="Objet de l'Intervention")
    decision_ids = fields.One2many('reclamationpgi.decision', 'intervention_id', string="Décisions")


class Deplacement(models.Model):
    _name = 'reclamationpgi.deplacement'
    _description = 'Déplacement'

    lieu = fields.Char(string="Lieu", required=True)
    actions = fields.Text(string="Actions", required=True)

class Decision(models.Model):
    _name = 'reclamationpgi.decision'
    _description = 'Décision'

    name = fields.Char(string="Objet de la Décision", required=True)
    signature = fields.Char(string="Signature", required=True)
    decision = fields.Text(string="Décision", required=True)
    statut = fields.Selection([
        ('en_cours', 'En Cours'),
        ('finalisee', 'Finalisée'),
        ('annulee', 'Annulée'),
    ], string="Statut", default='en_cours', required=True)
    
    membres_commission = fields.Many2many('hr.employee', string="Membres de la Commission")
    
    intervention_id = fields.Many2one('reclamationpgi.intervention', string="Intervention Associée", required=True)
    is_communicated = fields.Boolean(string='Communiqué ?', default=False)


class Communication(models.Model):
    _name = 'reclamationpgi.communication'
    _description = "Communication liée aux Réclamations"

    # Champs de communication
    type_communication = fields.Selection([
        ('mail', 'Email'),
        ('appel', 'Appel Téléphonique'),
        ('sms', 'SMS')
    ], string="Type de Communication", required=True)
    date = fields.Datetime(string="Date", required=True, default=fields.Datetime.now)
    motif = fields.Selection([
        ('infos complementaires', 'Demande d informations complementaires'),
        ('response', 'Reponse au reclamant'),
        ('decision', 'Information de la decision') , 
        ('pieces jointes', 'Manque de pieces justificatives ou erreur') , 
      
    ], string="Motif de la Communication", required=True)
    objet = fields.Text(string="Objet de la Communication", required=True)
    contenu = fields.Text(string="Contenu / Description", required=True)

    
    
     # Relations
    reclamation_id = fields.Many2one('reclamationpgi.reclamation', string="Réclamation", required=True)
    reclamant_id = fields.Many2one('reclamationpgi.reclamant', string="Réclamant" , required=True)
    reclamantmail = fields.Char(string="Reclamant Email")
    reclamantTel = fields.Char(string="Reclamant Phone")

# @api.onchange('reclamation_id')
# def _onchange_reclamation_id(self):
#         """Update fields based on the selected `reclamation_id`."""
#         for record in self:
#             if record.reclamation_id:
#                 reclamation = record.reclamation_id
#                 reclamant = reclamation.reclamant_id

#                 # Update reclamant details
#                 record.reclamant_id = reclamant.id if reclamant else False
#                 record.reclamantmail = (
#                     reclamant.reclamant_email or reclamant.company_email
#                 ) if reclamant else False
#                 record.reclamantTel = (
#                     reclamant.reclamant_phone or reclamant.company_phone
#                 ) if reclamant else False

#                 # Update agent details
#                 record.agent_id = reclamation.assigned_agent.id if reclamation.assigned_agent else False
#             else:
#                 # Clear fields if no reclamation is selected
#                 record.reclamant_id = False
#                 record.reclamantmail = False
#                 record.reclamantTel = False
#                 record.agent_id = False





# # @api.depends(
# #     'reclamation_id', 
# #     'reclamation_id.reclamant_id', 
# #     'reclamation_id.reclamant_id.reclamant_email', 
# #     'reclamation_id.reclamant_id.reclamant_phone', 
# #     'reclamation_id.assigned_agent'
# # )
# # def _compute_reclamant_details(self):
# #     for record in self:
# #         if record.reclamation_id:
# #             reclamant = record.reclamation_id.reclamant_id
# #             record.reclamant_id = reclamant
# #             record.reclamantmail = (
# #                 reclamant.reclamant_email or reclamant.company_email
# #             ) if reclamant else False
# #             record.reclamantTel = (
# #                 reclamant.reclamant_phone or reclamant.company_phone
# #             ) if reclamant else False
# #             record.agent_id = record.reclamation_id.assigned_agent
# #         else:
# #             record.reclamant_id = False
# #             record.reclamantmail = False
# #             record.reclamantTel = False
# #             record.agent_id = False
