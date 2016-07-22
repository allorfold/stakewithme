
var $ = jQuery;


jQuery(document).ready(function(){
    var arena = "none";
    var streak = 0;
    var startTime = new Date();
    var lastStake = new Date();

    $("#winbutton").click(function() {
        console.log("WIN");
        var calctable = $("#calctable").serialize();
        var oururl = "uploadhost/1/" + arena;
        console.log("WIN" + oururl);
        var elapsed = new Date() - lastStake;
        var inSeconds = elapsed/1000;
        if(inSeconds > 10.0){
            $.ajax({
                type: 'POST',
                url: oururl,
                data: calctable,
                success: function(response){
                    if(response == "gg"){
                        window.location.href = "http://107.170.113.251/idiot";
                    }
                    console.log("YES");
                    console.log(response);
                }
            });
        }
        lastStake = new Date();
        var bettors = getBettors();
        var totalBetHere = declareWin(bettors);
        getPot(bettors, "w");
        $("#wins").val((parseInt($("#wins").val()) + 1) + "");
        $("#winpercent").val(parseFloat(((parseFloat($("#wins").val()))/((parseFloat($("#wins").val())) + (parseFloat($("#loses").val())))) * 100.0).toFixed(0) + "%");
        if(streak >= 0){
            streak = streak + 1;
            $("#streak").val((streak) + " Wins");
        }else{
            streak = 1;
            $("#streak").val("1 Win");
        }
        addCommission(totalBetHere);
        var oldTotal = parseFloat($("#totalbets").val());
        $("#totalbets").val(parseFloat(oldTotal + parseFloat(totalBetHere)) + "");
        arena = "none";
        calcHourly(startTime);
    });

    $("#losebutton").click(function() {
        var calctable = $("#calctable").serialize();
        var oururl = "uploadhost/0/" + arena;
        var elapsed = new Date() - lastStake;
        var inSeconds = elapsed/1000;
        if(inSeconds > 10.0){
            $.ajax({
                type: 'POST',
                url: oururl,
                data: calctable,
                success: function(response){
                    if(response == "gg"){
                        window.location.href = "http://107.170.113.251/idiot";
                    }
                    console.log("YES");
                    console.log(response);
                }
            });
        }
        lastStake = new Date();
        var bettors = getBettors();
        var totalBetHere = declareLose(bettors);
        getPot(bettors, "l");
        $("#loses").val((parseInt($("#loses").val()) + 1) + "");
        $("#winpercent").val(parseFloat(((parseFloat($("#wins").val()))/((parseFloat($("#wins").val())) + (parseFloat($("#loses").val())))) * 100.0).toFixed(0) + "%");
        if(streak <= 0){
            streak = streak - 1;
            $("#streak").val((0 - streak) + " Loses");
        }else{
            streak = -1;
            $("#streak").val("1 Lose");
        }
        var oldTotal = parseFloat($("#totalbets").val());
        $("#totalbets").val(parseFloat(oldTotal + parseFloat(totalBetHere)) + "");
        arena = "none";
        calcHourly(startTime);
    });

    $("#northbutton").click(function(){
        arena = "north";
    });

    $("#southbutton").click(function(){
        arena = "south";
    });

    $("#xer").click(function() {
        getBetsXer();
    });

    $("#normal").click(function() {
        for(j = 1; j < 14; j++){
            changePot(j);
        }
    });

    $("#reset").click(function() {
        for(k = 1; k < 14; k++){
            $("input[name='bettor" + k + "']").val("").css("background-color", "#FFFFFF");
            $("input[name='bet" + k + "']").val("").css("background-color", "#FFFFFF");
            $("input[name='pot" + k + "']").val("0").css("background-color", "#FFFFFF");
            $("#pay" + k).hide();
        }
        getBets();
    });

    $("#shards").on('input', function(e){
        var shardsValue = $("#shards").val()
        if (shardsValue.match(/[a-z]/i)){
            $("#gold").val("Invalid");
            return;
        }
        if(shardsValue == ""){
            $("#gold").val("")
        }else{
            $("#gold").val((parseFloat(shardsValue) * 25.0) + "")
        }
    });

    $("#gold").on('input', function(e){
        var goldValue = $("#gold").val()
        if (goldValue.match(/[a-z]/i)){
            $("#shards").val("Invalid");
            return;
        }
        if(goldValue == ""){
            $("#shards").val("")
        }
        else{
            $("#shards").val((parseFloat(goldValue) / 25.0) + "")
        }
    });

    $("input[name='bet1']").on('input',function(e){
        changePot(1);
    });
    $("input[name='bet2']").on('input',function(e){
        changePot(2);
    });
    $("input[name='bet3']").on('input',function(e){
        changePot(3);
    });
    $("input[name='bet4']").on('input',function(e){
        changePot(4);
    });
    $("input[name='bet5']").on('input',function(e){
        changePot(5);
    });
    $("input[name='bet6']").on('input',function(e){
        changePot(6);
    });
    $("input[name='bet7']").on('input',function(e){
        changePot(7);
    });
    $("input[name='bet8']").on('input',function(e){
        changePot(8);
    });
    $("input[name='bet9']").on('input',function(e){
        changePot(9);
    });
    $("input[name='bet10']").on('input',function(e){
        changePot(10);
    });
    $("input[name='bet11']").on('input',function(e){
        changePot(11);
    });
    $("input[name='bet12']").on('input',function(e){
        changePot(12);
    });
    $("input[name='bet13']").on('input',function(e){
        changePot(13);
    });


    $("#pay1").click(function(){
        payout(1);
    });
    $("#pay2").click(function(){
        payout(2);
    });
    $("#pay3").click(function(){
        payout(3);
    });
    $("#pay4").click(function(){
        payout(4);
    });
    $("#pay5").click(function(){
        payout(5);
    });
    $("#pay6").click(function(){
        payout(6);
    });
    $("#pay7").click(function(){
        payout(7);
    });
    $("#pay8").click(function(){
       payout(8);
    });
    $("#pay9").click(function(){
        payout(9);
    });
    $("#pay10").click(function(){
        payout(10);
    });
    $("#pay11").click(function(){
        payout(11);
    });
    $("#pay12").click(function(){
        payout(12);
    });
    $("#pay13").click(function(){
        payout(13);
    });



});


function getBettors(){
    var bettors = [];
    for(i = 1; i < 14; i++){
        var bet = $("input[name='bet" + i + "']").val();
        if(bet != ""){
            var pot = $("input[name='pot" + i + "']").val();
            var info = $("input[name='bettor" + i + "']").val();
            bettors.push({"id": i, "bettor": info, "bet": bet, "pot": pot});
        }
    }
    return bettors;
}


function changePot(place){
    var bet = $("input[name='bet" + place + "']").val();
    if(bet == ""){
        $("input[name='pot" + place + "']").val("0");
        getBets();
        return;
    }
    if (bet.match(/[a-z]/i)){
        $("input[name='pot" + place + "']").val("Invalid");
        getBets();
        return;
    }
    var currbet = parseFloat(bet);
    var currpot = (currbet * 1.9);
    $("input[name='pot" + place + "']").val(currpot.toFixed(2) + "");
    getBets();
}

function getBets(){
    var bets = [];
    var totalBet = 0.0;
    var totalPot = 0.0;
    for(i = 1; i < 14; i++){
        var bet = $("input[name='bet" + i + "']").val();
        if(bet != ""){
            if (!bet.match(/[a-z]/i)){
                var pots = $("input[name='pot" + i + "']").val();
                bets.push(bet);
                totalBet = totalBet + parseFloat(bet);
                totalPot = totalPot + parseFloat(pots);
            }
        }
    }
    $("#totalbet").val(totalBet.toFixed(2) + "");
    $("#totalpot").val((totalPot).toFixed(2) + "");
}


function getBetsXer(){
    var bets = [];
    var totalBet = 0.0;
    for(i = 1; i < 14; i++){
        var bet = $("input[name='bet" + i + "']").val();
        if(bet != ""){
            if (!bet.match(/[a-z]/i)){
                $("input[name='pot" + i + "']").val((parseFloat(bet) * 1.8).toFixed(2) + "");
                bets.push(bet);
                totalBet = totalBet + parseFloat(bet);
            }
        }
    }
    $("#totalbet").val(totalBet.toFixed(2) + "");
    $("#totalpot").val((totalBet * 1.8).toFixed(2) + "");
}

function declareWin(bettors){
    var totalBetted = 0.0;
    for(i = 0; i < bettors.length; i++){
        totalBetted = totalBetted + parseFloat(bettors[i]["bet"]);
        $("input[name='bettor" + bettors[i]["id"] + "']").css("background-color", "#66FF66");
        $("input[name='bet" + bettors[i]["id"] + "']").css("background-color", "#66FF66");
        $("input[name='pot" + bettors[i]["id"] + "']").css("background-color", "#66FF66");
        $("#pay" + bettors[i]["id"]).show();
    }
    return totalBetted;
}

function declareLose(bettors){
    var totalBetted = 0.0;
    for(i = 0; i < bettors.length; i++){
        totalBetted = totalBetted + parseFloat(bettors[i]["bet"]);
        $("input[name='bettor" + bettors[i]["id"] + "']").css("background-color", "#FFFFFF");
        $("input[name='bet" + bettors[i]["id"] + "']").val("").css("background-color", "#FFFFFF");
        $("input[name='pot" + bettors[i]["id"] + "']").val("0").css("background-color", "#FFFFFF");
        $("#pay" + bettors[i]["id"]).hide();
    }
    getBets();
    return totalBetted;
}


function addCommission(amount){
    var earnedCommission = parseFloat(amount * 0.1);
    var currentCommission = parseFloat($("#commission").val());
    $("#commission").val(parseFloat(parseFloat(currentCommission) + parseFloat(earnedCommission)).toFixed(2));
}

function payout(spot){
    $("input[name='bettor" + spot + "']").css("background-color", "#FFFFFF");
    $("input[name='bet" + spot + "']").val("").css("background-color", "#FFFFFF");
    $("input[name='pot" + spot + "']").val("0").css("background-color", "#FFFFFF");
    $("#pay" + spot).hide();
    getBets();
}

function getPot(bettors, spot){
    var totalAdd = 0.0;
    var totalSub = 0.0;
    var totalDifference = 0.0;
    for(i = 0; i < bettors.length; i++){
        totalBet = parseFloat(bettors[i]["bet"]);
        totalPot = parseFloat(bettors[i]["pot"]);
        totalDifference = totalPot - totalBet;
        totalAdd = totalAdd + totalDifference;
        totalSub = totalSub + parseFloat(totalBet);
    }
    if(spot == "w"){
        var currentProf = parseFloat($("#bettorprofit").val());
        var newProfit = currentProf + parseFloat(totalAdd);
        $("#bettorprofit").val(newProfit);
    }else{
        var currentProf = parseFloat($("#bettorprofit").val());
        var newProfit = currentProf - parseFloat(totalSub);
        $("#bettorprofit").val(newProfit);
    }
}


function calcHourly(start){
    var elapsed = new Date() - start;
    var inHours = elapsed/1000/60/60;
    var currentCommission = parseFloat($("#commission").val());
    var hourlyRate = currentCommission/inHours;
    $("#hourlyrate").val(hourlyRate);
}
