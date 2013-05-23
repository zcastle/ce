Ext.define('sup.view.GridEmpresa', {
	extend: 'Ext.grid.Panel',
	alias: 'widget.gridEmpresa',
	store: 'Empresa',
	initComponent: function() {
		this.columns = [{
			header: 'RUC',
			dataIndex: 'nu_ruc',
			width: 80
		},{
			header: 'Razon Social',
			dataIndex: 'no_razon_social',
			flex: 1,
			renderer: function(text){
				return Ext.util.Format.uppercase(text);
			}
		},{
			header: 'Nombre Comercial',
			dataIndex: 'no_comercial',
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
			header: 'Email',
			dataIndex: 'email',
			width: 150
		},{
			header: 'Web',
			dataIndex: 'no_web',
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
            store: 'Empresa',
            displayInfo: true,
            displayMsg: 'Mostrando empresas {0} - {1} de {2}',
            emptyMsg: "No hay empresas para mostrar",
            items:[]
        });
		this.callParent(arguments);
	}
})