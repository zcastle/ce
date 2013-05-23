Ext.define('sup.view.TabMain', {
    extend: 'Ext.TabPanel',
    alias : 'widget.tabmain',
    layout: 'fit',
    autoShow: true,
    initComponent: function(){
        this.items = [];
        this.callParent(arguments);
    }
});