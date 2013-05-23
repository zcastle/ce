Ext.define('sup.view.GridPostulante', {
	extend: 'Ext.grid.Panel',
	alias: 'widget.gridPostulante',
	store: 'Postulante',
	initComponent: function() {
		this.columns = [{
			header: 'Nombre',
			dataIndex: 'no_postulante',
			width: 150,
			renderer: function(text){
				return Ext.util.Format.uppercase(text);
			}
		},{
			header: 'A. Paterno',
			dataIndex: 'ap_postulante',
			width: 150,
			renderer: function(text){
				return Ext.util.Format.uppercase(text);
			}
		},{
			header: 'A. Materno',
			dataIndex: 'am_postulante',
			width: 150,
			renderer: function(text){
				return Ext.util.Format.uppercase(text);
			}
		},{
			header: 'Nu. Fijo',
			dataIndex: 'nu_fijo',
			width: 80
		},{
			header: 'Nu. Movil',
			dataIndex: 'nu_movil',
			width: 80
		},{
			header: 'F. Nacimiento',
			dataIndex: 'fe_nacimiento',
			width: 80
		},{
			header: 'Email',
			dataIndex: 'email',
			width: 150
		},{
			header: 'Direccion',
			dataIndex: 'de_direccion',
			width: 200,
			renderer: function(text){
				return Ext.util.Format.uppercase(text);
			}
		},{
			header: 'Distrito',
			dataIndex: 'no_ubigeo',
			width: 200,
			renderer: function(text){
				return Ext.util.Format.uppercase(text);
			}
		}];
		this.bbar = Ext.create('Ext.PagingToolbar', {
            store: 'Postulante',
            displayInfo: true,
            displayMsg: 'Mostrando postulantes {0} - {1} de {2}',
            emptyMsg: "No hay postulantes para mostrar",
            items:[]
        });
		this.callParent(arguments);
	}
	
})