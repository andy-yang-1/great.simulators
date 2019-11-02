var R = new Array(0, 0, 0, 0, 0, 0, 0);
function onestep()
{
    for (var i = 6; i > 0; i--)
    {
        R[i] += R[i - 1];
    }
}
function backstep()
{
    for (var i = 0; i < 6; i++)
    {
        R[i+1] -= R[i];
    }
}
function showoff()
{
    for (var i = 0; i < 7; i++)
    {
        $("input[name='out" + i.toString() + "']").val(R[i]);
    }
}
$(document).ready(function ()
{
    $("#startcal").click(function ()
    {
        for (var i = 0; i <7; i++)
        {
            R[i] = Number($("input[name='re" + i.toString() + "']").val());
        }
        var T = $("input[name='times']").val();
        for (var i = 0; i < T; i++)
            onestep();
        showoff();
    });
    $("#nextstep").click(function ()
    {
        onestep();
        showoff();
    });
    $("#backstep").click(function ()
    {
        backstep();
        showoff();
    });
});