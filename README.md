# Projet-Odoo
----------------------------------------------------------1st commit ( apres clonage de la branche de rayane)
Major changes :
1-Reorganisation des fichiers en creant 2 dossiers Controllers et Reports

2-Modifications du model : Reclamation et de son fichier reclamation.xml
  -Ajout du champs provenance(appel,formulaire du site,presentiel) de la reclamation
  -Modification des champs "required" a fournir lors de la creation d'une Reclamation
  -Reajustement des vues liste, et form de Reclamation
  
3-Modifications du model : Reclamant et de son fichier reclamant.xml 
  -Ajouts des champs ( reclamant_email, reclamant_phone , company_code)
  -Modification des noms des champs concernant les reclamants de type 'individu'
  -Modification des champs et de l'affichage des vus liste,form du reclamant

4-Ajout de la fonctionnalite de Soumission de Reclamation via Le site Web 

5-Pour assuerer le bon fonctionnement du module lors des tests merci de :
-1 Activer mode devloppeur => Acceder a l'utilisateur admin => lui attribuer le role reclamation manager (situer tout en bas) afin que vous puissiez creer des reclamations
-2 Verifier que vous possedez au moins Une Company (entreprise ) du nom de 'My Company' (le champs concerné portera plus tard le nom de notre agence )
-3 intaller le module Site Web , choisir un theme quelconque (le menu du site web devrait afficher la fonctionnalité : Nouvelle Reclamation)
