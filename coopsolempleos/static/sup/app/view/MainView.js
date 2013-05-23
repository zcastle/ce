Ext.define('sup.view.MainView', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.mainview',
    layout: 'border',
    items: [{
        region: 'north',
        height: 65,
        border: false,
        items: [{
            xtype: 'image',
            src: '../static/images/logo.png'
        }]
    },{
        region: 'west',
        title: 'Opciones',
        width: 120,
        items: [{
            xtype: 'menu'
        }]
    },{
        region: 'center',
        id: 'contenedor',
        //title: 'Contenido',
        xtype: 'tabmain'
    },{
        region: 'south',
        title: 'Estado'
    }]
});