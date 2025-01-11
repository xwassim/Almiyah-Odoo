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

    # Agence
    agency_id = fields.Many2one('res.partner', string="Agence", required=True, help="Agence associée à la réclamation")

    # Origine de la réclamation
    origin = fields.Selection([
        ('citoyen', 'Citoyen'),
        ('entreprise', 'Entreprise'),
        ('cellule_veille', 'Cellule de Veille')
    ], string="Origine de la Réclamation", required=True)

    # Informations sur le réclamant
    reclamant_id = fields.Many2one('reclamationpgi.reclamant', string="Réclamant")

    # Assignation de l'agent
    assigned_agent = fields.Many2one('res.users', string="Agent Assigné", 
                                     help="Assigné automatiquement si la réclamation est saisie sur place.")

    # Statut de la réclamation
    status = fields.Selection([
        ('pending', 'En Attente'),
        ('processed', 'Traitée'),
        ('archived', 'Archivée')
    ], string="Statut", default='pending', required=True)

    # Priorité et complexité
    urgency = fields.Boolean(string="Urgence", default=False, help="Indique si la réclamation est urgente.")
    claim_type = fields.Selection([
        ('commercial', 'Commerciale'),
        ('technical', 'Technique')
    ], string="Type de Réclamation")
    complexity = fields.Selection([
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Élevée')
    ], string="Complexité")
    severity = fields.Selection([
        ('minor', 'Mineure'),
        ('major', 'Majeure'),
        ('critical', 'Critique')
    ], string="Gravité")

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
    ], string="Departement agent", required=True)

class Reclamant(models.Model):
    _name = 'reclamationpgi.reclamant'
    _description = "Informations sur le Réclamant"

    type = fields.Selection([
        ('individual', 'Individu'),
        ('enterprise', 'Entreprise')
    ], string="Type de Réclamant", required=True)

    # Fields for Individuals
    first_name = fields.Char(string="Prénom", states={'readonly': [('type', '!=', 'individual')]})
    last_name = fields.Char(string="Nom", states={'readonly': [('type', '!=', 'individual')]})
    address = fields.Text(string="Adresse", states={'readonly': [('type', '!=', 'individual')]})
    city = fields.Char(string="Commune", states={'readonly': [('type', '!=', 'individual')]})

    # Fields for Enterprises
    company_name = fields.Char(string="Nom de l'Entreprise", states={'readonly': [('type', '!=', 'enterprise')]})
    company_address = fields.Text(string="Adresse de l'Entreprise", states={'readonly': [('type', '!=', 'enterprise')]})
    company_phone = fields.Char(string="Téléphone de l'Entreprise", states={'readonly': [('type', '!=', 'enterprise')]})
    company_email = fields.Char(string="Email de l'Entreprise", states={'readonly': [('type', '!=', 'enterprise')]})
    company_sector = fields.Char(string="Secteur d'Activité", states={'readonly': [('type', '!=', 'enterprise')]})

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
