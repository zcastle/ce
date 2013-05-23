Ext.define('sup.view.GridEmpleo', {
	extend: 'Ext.grid.Panel',
	alias: 'widget.gridEmpleo',
	store: 'Empleo',
	initComponent: function() {
		this.columns = [{
			header: 'Empleo',
			dataIndex: 'no_empleo',
			flex: 1,
			renderer: function(text){
				return Ext.util.Format.uppercase(text);
			}
		},{
			header: 'Descripcion',
			dataIndex: 'de_empleo',
			flex: 1,
			renderer: function(text){
				return Ext.util.Format.uppercase(text);
			}
		},{
			header: 'Sueldo',
			dataIndex: 'va_sueldo',
			align: 'right',
			width: 80
		},{
			header: 'Creacion',
			dataIndex: 'fe_creacion',
			width: 80
		},{
			header: 'Area',
			dataIndex: 'no_area',
			width: 150,
			renderer: function(text){
				return Ext.util.Format.uppercase(text);
			}
		},{
			header: 'Tipo Empleo',
			dataIndex: 'no_tipoempleo',
			width: 120,
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
            store: 'Empleo',
            displayInfo: true,
            displayMsg: 'Mostrando empleos {0} - {1} de {2}',
            emptyMsg: "No hay empleos para mostrar",
            items:[]
        });
		this.callParent(arguments);
	}
})