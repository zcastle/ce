Ext.define('sup.store.Postulante', {
    extend: 'Ext.data.Store',
    model: 'sup.model.Postulante',
    pageSize: 10,
    proxy: {
        noCache: false,
        type: 'ajax',
        api: {
            read: '/sup/postulante_json'
        },
        reader: {
            type: 'json',
            root: 'postulante',
            successProperty: 'success',
            totalProperty: 'totalCount'
        },
        actionMethods: {
            read: 'POST'
        }
    }
});