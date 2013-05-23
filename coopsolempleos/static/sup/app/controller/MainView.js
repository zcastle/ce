Ext.define('sup.controller.MainView', {
    extend: 'Ext.app.Controller',
    views: [
    'MainView',
    'Menu',
    'GridPostulante',
    'GridEmpresa',
    'GridEmpleo',
    'TabMain'
    ],
    stores: [
        'Postulante',
        'Empresa',
        'Empleo'
    ],
    init: function() {
        this.control({
            'mainview': {
                render: this.onMainViewRendered
            },
            'menu button': {
                click: this.onMenuClickItem
            }
        });
    },
    onMainViewRendered: function() {
        this.getController('TabMain').addTab('Postulantes', 'gridPostulante');
        this.getPostulanteStore().load();
        this.getEmpresaStore().load();
        this.getEmpleoStore().load();
    },
    onMenuClickItem: function(menuItem){
        switch(menuItem.action){
            case 'mnuPostulante':
                this.getController('TabMain').addTab(menuItem.text, 'gridPostulante')
                break;
            case 'mnuEmpresa':
                this.getController('TabMain').addTab(menuItem.text, 'gridEmpresa')
                break;
            case 'mnuEmpleo':
                this.getController('TabMain').addTab(menuItem.text, 'gridEmpleo')
                break;
        }
    }
});