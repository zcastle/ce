Ext.define('sup.store.Empresa', {
    extend: 'Ext.data.Store',
    model: 'sup.model.Empresa',
    pageSize: 10,
    proxy: {
        noCache: false,
        type: 'ajax',
        api: {
            read: '/sup/empresa_json'
        },
        reader: {
            type: 'json',
            root: 'empresa',
            successProperty: 'success',
            totalProperty: 'totalCount'
        },
        actionMethods: {
            read: 'POST'
        }
    }
});