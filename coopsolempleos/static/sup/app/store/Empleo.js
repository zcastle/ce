Ext.define('sup.store.Empleo', {
    extend: 'Ext.data.Store',
    model: 'sup.model.Empleo',
    pageSize: 10,
    proxy: {
        noCache: false,
        type: 'ajax',
        api: {
            read: '/sup/empleo_json'
        },
        reader: {
            type: 'json',
            root: 'empleo',
            successProperty: 'success',
            totalProperty: 'totalCount'
        },
        actionMethods: {
            read: 'POST'
        }
    }
});