
<!DOCTYPE html>
<html>
<head lang="en">
    <title>Delete Task</title>
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
             <li><a href="/app/new" title="Add a new task">New</a></li>
         </ul>
    </nav>
    <section>
        <br>
        <br>
        <div class="alert alert-warning">
                Delete task {{id}}?
        </div>
        <br>
        <form action="/app/delete/{{id}}" method="POST"class="form-horizontal" role="form">
            <div class="form-group">
                <label class="control-label col-sm-1" for="id">ID:</label>
                <div class="col-sm-2">
                    <input type="text" class="form-control" id="id" name="id" value="{{task['id']}}" disabled>
                </div>
            </div>
            <div class="form-group">
                <label class="control-label col-sm-1" for="summary">Summary:</label>
                <div class="col-sm-6">
                    <input type="text" class="form-control" id="summary" name="summary" value="{{task['summary']}}" size="80"
                           maxlength="100" disabled>
                </div>
            </div>
            <div class="form-group">
                <label class="control-label col-sm-1" for="description">Description:</label>
                <div class="col-sm-10">
                    <textarea class="form-control" rows="5" id="description" name="description" maxlength="1000" disabled>{{task['description']}}</textarea>
                </div>
            </div>
            <div class="form-group">
                <label class="control-label col-sm-1" for="duedate">Due date:</label>
                <div class="col-sm-2">
                    <input type="date" class="form-control" id="duedate" name="duedate" value="{{task['duedate']}}" disabled>
                </div>
            </div>
            <div class="form-group">
                <label class="control-label col-sm-1" for="status">Status:</label>
                <div class="col-sm-2">
                    <select class="form-control" id="status" name="status" disabled>
                        %if task['status_id'] == 'O':
                        <option value="open" selected>Open</option>
                        <option value="closed">Closed</option>
                        %else:
                        <option value="open">Open</option>
                        <option value="closed" selected>Closed</option>
                        %end
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label class="control-label col-sm-1">Modified:</label>
                <div class="col-sm-3">
                    <p class="form-control-static">{{task['modified']}}</p>
                </div>
            </div>
            <br>
            <div class="form-group">
                <div class="col-sm-offset-1 col-sm-10">
                    <button type="submit" class="btn btn-default" name="answer" value="yes">Yes</button>
                    <button type="submit" class="btn btn-default" name="answer" value="no" autofocus>No</button>
                </div>
            </div>
        </form>
    </section>
</div>
</body>
</html>