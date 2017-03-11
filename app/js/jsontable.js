(function ( $ ) {
    var settings = {
        datas: {
            urlData: null,
            term: "",
            dataSet: null,
        },
                
        table: {
            headRowSelector: "thead tr",
            ref: null, 
            columns: null,
            columnsLength: null,
            
            writers: {
                rowWriter: defaultRowWriter,
                cellWriter: defaultCellWriter,
            }
        }
    };

    $.fn.jsonTable = function(options) {    
        settings = $.extend(true, settings, options);
        settings.table.ref = this;
        
        parseColumnsHeader();
        
        jsonDownload();
        
        return this;
    };
    
    $.fn.jsonTable.update = function() {
        jsonDownload();
    }
    
    $.fn.jsonTable.search = function(term) {
        settings.datas.term = term.trim();
        jsonDownload();
    };
    
    $.fn.jsonTable.getKeyFromColumnId = function(columnIndex) {
        return settings.table.columns[columnIndex];
    }
    
    function parseColumnsHeader() {
        settings.table.columns = {};
        settings.table.columnsLength = 0;
        
        settings.table.ref.find(settings.table.headRowSelector).children("th, td").each(function(index) {
            var valueAttr = $(this).attr("data-jsontable-attr");
            if(valueAttr === undefined) //TODO: gérer ça avec la normalisation 
                $.error("Column " +index + " doesn't have a 'data-jsontable-attr' attribute");
            else {
                settings.table.columns[index] = valueAttr;
                settings.table.columnsLength++;
            }              
        });

    }
        
    function jsonDownload() {
        $.ajax({
            url : settings.datas.urlData,          /* URL du script */
            dataType : 'json', 

            data : {
                term : settings.datas.term
            },

            /* Dès que requête a aboutie, on recherche si la valeur existe bien dans la DB */
            success : function(data) {
                settings.datas.dataSet = data;
                updateTable();
            }
        });
    }
    
    function updateTable() {
        var tBody = settings.table.ref.find("tbody");
        
        tBody.find("tr").remove();
        
        $.each(settings.datas.dataSet, function(i, obj) {
            tBody.append(settings.table.writers.rowWriter(i, obj));
        });
    }
    
    function defaultRowWriter(rowIndex, record) {
        var htmlCode = "<tr id='ri" + rowIndex + "'>\n";

        for (var columnIndex=0; columnIndex < settings.table.columnsLength; columnIndex++) {
            htmlCode += settings.table.writers.cellWriter(columnIndex, record);
        }
        
        htmlCode += "</tr>\n";
        return htmlCode;
    }
    
    function defaultCellWriter(columnIndex, record) {
        var htmlCode = "<td>";

        var val = record[$.fn.jsonTable.getKeyFromColumnId(columnIndex)];
        if(val !== null && val !== undefined)
            htmlCode += val;
        
        htmlCode += "</td>\n";
        
        return htmlCode;
    }
}( jQuery ));