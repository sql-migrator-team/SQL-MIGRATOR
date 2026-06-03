const ctx =
document.getElementById(
'migrationChart'
);

new Chart(ctx, {

type:'line',

data:{

labels:[
'May1',
'May5',
'May10',
'May15',
'May20',
'May25',
'May30'
],

datasets:[

{
label:'Successful',
data:[20,35,28,38,30,36,40],
borderColor:'green'
},

{
label:'Warnings',
data:[10,14,11,15,12,14,10],
borderColor:'orange'
},

{
label:'Failed',
data:[3,5,4,5,4,6,3],
borderColor:'red'
}

]

}

});
