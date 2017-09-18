<!-- template for the form for a new task -->
<!DOCTYPE html>
<html>
<head lang="en">
    <title>New Task</title>
    %include("header.tpl")
</head>
<body>
<div class="container-fluid">
    <header class="well">
        <h1>Tasklist</h1>
    </header>
    <nav>
         <ul class="nav nav-pills">
             <li><a href="/app/list" title="Show the todo list">List</a></li>
             <li class="active"><a href="/app/new" title="Add a new task">New</a></li>
         </ul>
    </nav>
    <section>
        <form action="/app/new" method="POST" class="form-horizontal" role="form">
            <br>
            <br>
            <div class="alert alert-info">
                Add new task
            </div>
            <br>

            <div class="form-group">
                <label class="control-label col-sm-1" for="id">ID:</label>
                <div class="col-sm-2">
                    <input type="text" class="form-control" id="id" name="id" disabled>
                </div>
            </div>
            <div class="form-group">
                <label class="control-label col-sm-1" for="summary">Summary:</label>
                <div class="col-sm-6">
                    <input type="text" class="form-control"  id="summary" name="summary" size="80" maxlength="100"
                           title="Task summary">
                </div>
            </div>
            <div class="form-group">
                <label class="control-label col-sm-1" for="description">Description:</label>
                <div class="col-sm-10">
                    <textarea class="form-control" rows="5" id="description" name="description" maxlength="1000"></textarea>
                </div>
            </div>
            <div class="form-group">
                <label class="control-label col-sm-1" for="duedate">Due-date:</label>
                <div class="col-sm-2">
                    <input type="date" class="form-control"  id="duedate" name="duedate" title="Date in 2015" required>
                </div>
            </div>
            <div class="form-group">
                <label class="control-label col-sm-1" for="status">Status:</label>
                <div class="col-sm-2">
                    <select class="form-control" id="status" name="status">
                        <option value="open" selected>Open</option>
                        <option value="closed">Closed</option>
                    </select>
                </div>
            </div>
            <br>
            <div class="form-group">
                <div class="col-sm-offset-1 col-sm-10">
                    <input type="submit" class="btn btn-default" name="save" value="Save">
                </div>
            </div>
        </form>
    </section>
</div>
</body>
</html>
