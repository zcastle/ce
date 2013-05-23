Ext.define('sup.view.Menu',{
	extend: 'Ext.toolbar.Toolbar',
	alias: 'widget.menu',
	vertical: true,
	defaults: {
		textAlign: 'left'
	},
	items: [{
        text: 'Postulantes',
        action: 'mnuPostulante'
    },{
        text: 'Empresas',
        action: 'mnuEmpresa'
    },{
        text: 'Empleos',
        action: 'mnuEmpleo'
    }]
})