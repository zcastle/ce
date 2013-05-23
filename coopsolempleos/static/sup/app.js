Ext.application({
    name: 'sup',
    appFolder: '/static/sup/app',
    launch: function() {
        Ext.create('Ext.container.Viewport', {
            layout: 'fit',
            items: [{
                    xtype: 'mainview'
                }
            ]
        });
    },
    controllers: [
    'MainView',
    'TabMain'
    ]
});
Ext.onReady(function() {
    Ext.require(["Ext.util.Cookies", "Ext.Ajax"], function(){
        // Add csrf token to every ajax request
        var token = Ext.util.Cookies.get('csrftoken');
        if(!token){
            Ext.Error.raise("Missing csrftoken cookie");
        } else {
            Ext.Ajax.defaultHeaders = Ext.apply(Ext.Ajax.defaultHeaders || {}, {
                'X-CSRFToken': token
            });
        }
    });
    (Ext.defer(function() {
        var hideMask = function () {
            Ext.get('loading').remove();
            Ext.fly('loading-mask').animate({
                opacity: 0,
                remove: true
            });
        };
        Ext.defer(hideMask, 250);
    },500));
});