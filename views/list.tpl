<!-- Show all tasks, and allow edit and delete via icons -->
<!DOCTYPE html>
<html>
<head lang="en">
    <title>Task List</title>
    %include("header.tpl")
   	<script>
		$(document).ready(function () {
			var grid = $("#grid-data").bootgrid({
				formatters: {
					"commands": function(column, row) {
						return "<button type=\"button\" class=\"btn btn-xs btn-default command-edit\" data-row-id=\"" + row.id + "\"><span class=\"fa fa-pencil\"></span></button> " +
       						"<button type=\"button\" class=\"btn btn-xs btn-default command-delete\" data-row-id=\"" + row.id + "\"><span class=\"fa fa-trash-o\"></span></button>";
					}
				}
			}).on("loaded.rs.jquery.bootgrid", function() {
				/* Executes after data is loaded and rendered */
				grid.find(".command-edit").on("click", function(e) {
					window.location.href = "/app/edit/" +  $(this).data("row-id");
				}).end().find(".command-delete").on("click", function(e) {
					window.location.href = "/app/delete/" +  $(this).data("row-id");
				});
			});
		});
	</script>
</head>
<body>
<div class="container-fluid">
    <header class="well">
        <h1>Tasklist</h1>
    </header>
     <nav>
         <ul class="nav nav-pills">
             <li class="active"><a href="/app/list" title="Show the todo list">List</a></li>
             <li><a href="/app/new" title="Add a new task">New</a></li>
         </ul>
     </nav>
    <section>
        <table id="grid-data" class="table table-condensed table-hover table-striped">
            <thead>
                <tr>
                    <th data-column-id="id" data-type="numeric" data-order="asc">ID</th>
                    <th data-column-id="summary">Summary</th>
                    <th data-column-id="duedate">Due date</th>
                    <th data-column-id="status">Status</th>
                    <th data-column-id="commands" data-formatter="commands" data-sortable="false">Commands</th>
                </tr>
            </thead>
            <tbody>
                %for task in tasks:
                <tr>
                    <td>{{task["id"]}}</td>
                    <td>{{task["summary"]}}</td>
                    <td>{{task["duedate"]}}</td>
                    <td>{{task["status_id"]}}</td>
                </tr>
                %end
            </tbody>
        </table>
    </section>
</div>
</body>
</html>