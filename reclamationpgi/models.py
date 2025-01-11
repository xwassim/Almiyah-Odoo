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
    ], string="Provenance de la réclamation")

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
        ], string="Rôle", help="Rôle de l'agent dans l'organisation.")
        
        department = fields.Selection([
        ('commercial', 'Commerciale'),
        ('technical', 'Technique')
    ], string="Departement agent", required=True)

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
    company_code = fields.Char(string="Raison social",states={'readonly': [('type', '!=', 'entreprise')]})

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
        ('infos complémentaires', 'Demande d’informations complémentaires'),
        ('response', 'Réponse au réclamant'),
        ('decision', 'Information de la décision')
    ], string="Motif de la Communication", required=True)
    contenu = fields.Text(string="Contenu / Description", required=True)
    
    # Relations
    reclamation_id = fields.Many2one('reclamationpgi.reclamation', string="Réclamation", required=True)
    reclamant_id = fields.Many2one('reclamationpgi.reclamant', string="Réclamant", required=True)
