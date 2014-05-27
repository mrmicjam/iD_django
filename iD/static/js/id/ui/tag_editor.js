iD.ui.TagEditor = function(context, entity) {
    var event = d3.dispatch('changeTags', 'choose', 'close'),
        presets = context.presets(),
        id = entity.id,
        tags = _.clone(entity.tags),
        preset,
        selection_,
        presetUI,
        tagList;

    function update() {
        var entity = context.hasEntity(id);
        if (!entity) return;

        tags = _.clone(entity.tags);

        // change preset if necessary (undos/redos)
        var newmatch = presets.match(entity, context.graph());
        if (newmatch !== preset) {
            tageditor(selection_, newmatch);
            return;
        }

        presetUI.change(tags);
        tagList.tags(tags);
    }

    function tageditor(selection, newpreset) {
        selection_ = selection;
        var geometry = entity.geometry(context.graph());

        if (!preset) preset = presets.match(entity, context.graph());

        // preset was explicitly chosen
        if (newpreset) {
            tags = preset.removeTags(tags, geometry);

            newpreset.applyTags(tags, geometry);
            preset = newpreset;
        }

        selection
            .datum(preset)
            .html('');

        var messagewrap = selection.append('div')
            .attr('class', 'header fillL cf');

        messagewrap.append('button')
            .attr('class', 'preset-reset fl ')
            .on('click', function() {
                event.choose(preset);
            })
            .append('span')
            .attr('class', 'icon back');

        messagewrap.append('h3')
            .attr('class', 'inspector-inner')
            .text(t('inspector.editing_feature', { feature: preset.name() }));

        messagewrap.append('button')
            .attr('class', 'preset-close fr')
            .on('click', event.close)
            .append('span')
            .attr('class', 'icon close');

        var editorwrap = selection.append('div')
            .attr('class', 'tag-wrap inspector-body fillL2 inspector-body-' + geometry);

        editorwrap.append('div')
            .attr('class', 'col12 inspector-inner preset-icon-wrap')
            .append('div')
            .attr('class','fillL')
            .call(iD.ui.PresetIcon(context.geometry(entity.id)));

        presetUI = iD.ui.preset(context, entity, preset)
            .on('change', changeTags)
            .on('close', event.close);

        tagList = iD.ui.Taglist(context, entity)
            .on('change', changeTags);

        var tageditorpreset = editorwrap.append('div')
            .attr('class', 'inspector-preset cf fillL col12')
            .call(presetUI);

        editorwrap.append('div')
            .attr('class', 'inspector-inner col12 additional-tags')
            .call(tagList, preset.id === 'other');

        if (!entity.isNew()) {
            var osmLink = tageditorpreset.append('div')
                .attr('class', 'col12 inspector-inner')
                .append('a')
                .attr('href', context.connection().entityURL(entity))
                .attr('target', '_blank');

            osmLink.append('span')
                .attr('class','icon icon-pre-text out-link');

            osmLink.append('span').text(t('inspector.view_on_osm'));
        }

        presetUI.change(tags);
        tagList.tags(tags);

        changeTags();

        context.history()
            .on('change.tag-editor', update);
    }

    function clean(o) {
        var out = {};
        for (var k in o) {
            var v = o[k].trim();
            if (v) out[k] = v;
        }
        return out;
    }

    function changeTags(changed) {
        tags = clean(_.extend(tags, changed));
        event.changeTags(_.clone(tags));
    }

    tageditor.close = function() {
        // Blur focused element so that tag changes are dispatched
        // See #1295
        document.activeElement.blur();

        // Firefox incorrectly implements blur, so typeahead elements
        // are not correctly removed. Remove any stragglers manually.
        d3.selectAll('div.typeahead').remove();

        context.history()
            .on('change.tag-editor', null);
    };

    return d3.rebind(tageditor, event, 'on');
};
