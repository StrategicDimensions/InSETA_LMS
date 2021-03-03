<h1>NLRD</h1>
<h2 style="Background:Red;">
    welcome to NLRD hell young developer... You have many challenges ahead. play wisely....or perish.
</h2>
<h3>index of pain</h3>
<ol>
    <li>first rule is always make a record in the nlrd.report model for any changes made in master data.</li>
    <li>the second rule is to be as fast as possible </li>
    <li>the third rule is to look for patterns that align and dig to find a common route cause for a whole pattern instead of just fixing the side effect</li>
    <li>you need to document new issues in this readme and propose a fix which needs to be verified</li>
    <li>this rule is the same as number 2 lol </li>
</ol>
<h3>this is where we list issues</h3>
<ol>
    <li>file 21
        <ol>
            <li>@varun no providers have a type set at all, its required, there isnt a U option</li>
            <li>@varun provider_class_id is blanket set to unknown</li>
        </ol>
    </li>
    <li>
    <li>file 26
        <ol>
            <li>allowed for setting an alt id type if an alt id is provided(national_id,passport_id), sets to passport_number</li>
        </ol>
    </li>
    <li>
    <strong>file 25</strong>
        <ol>
            <li>learner has no equity-"-blanket on equity as unknown"</li>
            <li>@varun what do we do about people with just dots in the address fields?
             there is no unknown prov to use.</li>
            <li>@varun no id num , gender, dob, home lang code, id attachment to solve dob,gender etc
            -http://localhost:8080/web?debug#id=397857&view_type=form&model=hr.employee</li>
            <li>assessor has no national id - some have passport nums http://localhost:8080/web?debug#id=406775&view_type=form&model=hr.employee</li>
            <li>@varun need to fill this suburb to fix at least one rec, add a province to it-
            http://localhost:8080/web?#id=10314&view_type=form&model=res.suburb&menu_id=415&action=448</li>
            <li>@varun as above-http://localhost:8080/web?#id=10341&view_type=form&model=res.suburb&menu_id=415&action=448</li>
            <li>@varun there are 95 suburbs with no provinces, if we set them the code should be able to bulk fix a few provinces</li>
            <li>@varun check for records where stat_msg doesnt contain "province"</li>
        </ol>
    </li>
    <li>file 29
        <ol>
            <li></li>
            <li></li>
        </ol>
    </li>
</ol>
<h3>notes:</h3>

<ol>
    <li>in nlrdv2.py there is a global called LOGIT, 
    enable this to make report records while generating the nlrd data,
    experimental</li>
    <li>buffed reporting to group by error type and allowed for names to be classified</li>
</ol>