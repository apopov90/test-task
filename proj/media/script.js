date_fields = [];
skeleton_map = new Array();

Object.size = function (obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function appendNew(id, data) {
    row = $('<tr>');
    id_ = $('<td>').text(id);
    row.append(id_);

    for (k in data) {
        col = $('<td>').text(data[k]['value']);
        row.append(col);
    }
    $('.right > table').find('tbody').append(row);
}

function reinit_view(r) {
    date_fields = [];
    skeleton_map = new Array();
    table = $('<table>');
    add_form = $('<form><fieldset><legend>Новая запись в таблицу "' + table_name + '"</legend><table></table></fieldset></form>');
    head = $('<tr>');

    for (k in r['structure']) {
        col = $('<th>');
        col.text(r['structure'][k]['name']);
        date_fields.push(r['structure'][k]['date'] ? 1 : 0);
        skeleton_map.push(r['structure'][k]['model_field']);
        head.append(col);
        add_form.find('table').append(r['structure'][k]['model_field'] == "id" ? null :
            $('<tr><td></td><td><input /></td></tr>')
                .find('input')
                .prop('type', 'text')
                .prop('name', r['structure'][k]['model_field'])
                .prop('name', r['structure'][k]['model_field'])
                .parents('tr')
                .find('td:first')
                .text(r['structure'][k]['name'])
                .parents('tr')
        )
        if (r['structure'][k]['date']) add_form.find('input:last').datepicker({ dateFormat: "yy-mm-dd" });
    }
    body = $('<tbody>');
    head.appendTo(body);

    for (k in r['content']) {
        row = $('<tr>');
        row.data('identifier', r['content'][k]['id']);
        for (s = 0; s < Object.size(skeleton_map); s++) {
            row.append($('<td>'));
        }
        for (s in r['content'][k]) {
            row.find('td:eq(' + skeleton_map.indexOf(s) + ')').text(r['content'][k][s] == null ? "" : r['content'][k][s]);
        }
        row.appendTo(body);
    }

    body.appendTo(table);

    add_new = $('<input>').prop('type', 'button').val('Добавить');
    add_new.appendTo(add_form.find('fieldset'));
    add_new.click(function () {
        data_ = $(this).parents('form').serialize();
        data_ += "&model=" + model_name;
        $.ajax({
            url: add_to_model,
            type: 'get',
            datatype: 'json',
            data: data_,
            success: function (d) {
                $('fieldset td span').remove();
                if (d['status'] != "OK") {
                    for (k in d['status']) {
                        $('<span>').text(d['status'][k][0]).insertAfter($('fieldset input[name=' + k + ']'));
                    }
                }
                else {
                    appendNew(d['id'], add_new.parents('form').serializeArray());
                    add_new.parents('form')[0].reset();
                    alert('Новая запись успешно добавлена');
                }
            }
        });
    });
    $('.right').html(table);
    $('.right').append(add_form);
}

$(document).ready(function () {
    table_name = null;
    model_name = null;
    $('.load-model').click(function () {
        ths_ = $(this);
        table_name = ths_.text();
        model_name = $(this).data('model');
        $.ajax({
            url: loadmodel,
            type: 'get',
            datatype: 'json',
            data: {'model': model_name},
            success: function (d) {
                $('.load-model').css('font-weight', 'normal');
                ths_.css('font-weight', 'bold');
                reinit_view(d)
            }
        });
    });
    $('.right > table td:not(:first-child)').live('click', function () {
        value_was = $(this).text();
        correct = true;
        if ($(this).children().length == 0) {
            column_index = $(this).index();
            if (!date_fields[column_index]) {
                input_ = $('<input type="text">');
                input_.val($(this).text());

                input_.blur(function () {
                    id = $(this).parents('tr').data('identifier');
                    value = $(this).val();
                    if (value != value_was) {
                        field = skeleton_map[column_index];
                        $.ajax({
                            url: updateobject,
                            type: 'get',
                            datatype: 'json',
                            async: false,
                            data: {'model': model_name,
                                'id': id,
                                'value': value == "" ? null : value,
                                'field': field
                            },
                            success: function (d) {
                                if (d['status'] != "OK") {
                                    alert(d['status'][field]);
                                    correct = false;
                                }
                            }
                        });
                    }
                    $(this).parent().text(correct ? $(this).val() : value_was);
                });
                $(this).html(input_);
                input_.focus();
            }
            else {
                input_ = $('<input type="text">');
                date_ = $(this).text();
                input_.val(date_);

                input_.datepicker({ dateFormat: "yy-mm-dd" });
                $(this).html(input_);
                input_.datepicker("option", "onClose", function () {
                    $(this).datepicker("hide");
                    $(this).parent().text(value_was);
                });

                input_.datepicker("setDate", date_);
                input_.datepicker("option", "onSelect", function () {
                    id = $(this).parents('tr').data('identifier');
                    value = $(this).datepicker({ dateFormat: 'dd-mm-yy' }).val();
                    if (value != value_was) {
                        field = skeleton_map[column_index];
                        $.ajax({
                            url: updateobject,
                            type: 'get',
                            datatype: 'json',
                            async: false,
                            data: {'model': model_name,
                                'id': id,
                                'value': value == "" ? null : value,
                                'field': field
                            },
                            success: function (d) {
                                if (d['status'] != "OK") {
                                    alert(d['status'][field]);
                                    correct = false;
                                }
                            }
                        });
                    }
                    $(this).parent().text(correct ? $(this).datepicker({ dateFormat: 'dd-mm-yy' }).val() : value_was);
                });
                input_.datepicker("show");
            }
        }
    });
});