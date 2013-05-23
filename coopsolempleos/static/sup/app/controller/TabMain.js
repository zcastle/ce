Ext.define('sup.controller.TabMain', {
    extend: 'Ext.app.Controller',
    views: [
    'TabMain'
    ],
    refs: [{
        ref: 'MainView',
        selector: 'tabmain'
    }],
    init: function() {
        this.control({
            'tabmain': {
                render: this.onTabMainRendered
            }
        });
    },
    onTabMainRendered: function() {
    },
    addTab: function(titulo, modulo, ico){
        if(Ext.getCmp('launcher')){
            Ext.getCmp('launcher').collapse();
        }
        var mainTabs = this.getMainView();
        for (i = 0; i <= mainTabs.items.getCount()-1; i++) {
            if(mainTabs.items.get(i).title==titulo){
                mainTabs.setActiveTab(mainTabs.items.get(i));
                return;
            }
        }
        var obj = Ext.widget(modulo);
        var tab = mainTabs.add({
            title: titulo,
            closable: true,
            iconCls: ico,
            layout: 'fit',
            items: obj
        });
        mainTabs.setActiveTab(tab);
    },
    addTab_url: function(titulo, url){
        var mainTabs = this.getMainView();
        for (i = 0; i <= mainTabs.items.getCount()-1; i++) {
            if(mainTabs.items.get(i).title==titulo){
                mainTabs.setActiveTab(mainTabs.items.get(i));
                return;
            }
        }
        //var obj = Ext.widget(modulo);
        var tab = mainTabs.add({
            title: titulo,
            closable: true,
            iconCls: 'tabs',
            layout: 'fit',
            url: url
        });
        mainTabs.setActiveTab(tab);
    }
});