This is for legacy, it's doesn't work for DSM 6.x and later.

This was a application created for Synology DSM 5.x that manages backups. 

This is based on a patched version of rsync that can detect file movement (to avoid uploading files that were simply moved). The synchronization took place between two synology. In "etc/rsync.includes", I put the name of the encrypted directory (@Directory @ / ***) in order to save encrypted files with ecrypt-fs (not the plain text version). As a result, without re-encryption, the data was backed up remotely in a encrypted form.

I used the following ressources to create this project :

 - The icon of the project is derived of http://www.iconspedia.com/icon/cloud-upload-vector-icon-44439.html : P.J. Onori, http://www.somerandomdude.com/
 - rsync-patched (bin/rsync-patched-{cli|srv}) : work the user "Benibur" from www.NAS-forum.com - http://www.nas-forum.com/forum/topic/18840-miroir-via-rsync-optimis-pour-les-dbits-faibles-wan/
 - rsync : Samba Rsybc - https://rsync.samba.org/
 - ssh-wrapper (bin/ssh-wrapper.sh) : Wallix - http://www.wallix.org/2011/10/18/restricting-remote-commands-over-ssh/
 - Javascript JQuery (app/js/jquery-1.11.0.min.js) : JQuery - https://jquery.com/
 - Javascript JSONTable (app/js/jsontable.js) : omkarkhair - https://github.com/omkarkhair/jsonTable
 - CSS Styles (app/css/pure-min-0.5.0.css) : Yahoo - htts://purecss.io/
 - Status images (app/images/status_*.png) : Synology
 - Somes others images : FamFamFam - http://www.famfamfam.com/lab/icons/silk/
 
 - DSM Developper Guide : Synology - https://www.synology.com/fr-fr/support/developer#tool
 - Source of "Subliminal" SPK by SynoCommunity : SynoCommunity - https://github.com/SynoCommunity/spksrc/tree/develop/spk/subliminal/src/app

Thank you !