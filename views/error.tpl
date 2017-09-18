<!-- Display an error message -->
<!DOCTYPE html>
<html>
<head lang="en">
    <title>Error</title>
    %include("header.tpl")
</head>
<body>
<div class="container-fluid">
    <header class="well">
        <h4>Error</h4>
    </header>
    <section>
        <br>
        <br>
        <div class="alert alert-danger">
            %if "status" in result:
                status: {{result["status"]}} <br>
            %end
            %if "message" in result:
                message: {{result["message"]}} <br>
            %end
            %if "code" in result:
                code: {{result["code"]}} <br>
            %end
            %if "data" in result:
                data: {{result["data"]}} <br>
            %end
        </div>
    </section>
</div>
</body>
</html>