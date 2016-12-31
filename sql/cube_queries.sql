select t2.size as "Size", t1.* 
  from mc t1
  join (select axis1,  axis2, axis3, count(*) as size
          from mc
         group by axis1, axis2, axis3) t2
    on t2.axis1 = t1.axis1
   and t2.axis2 = t1.axis2
   and t2.axis3 = t1.axis3
 order by t2.size desc, t1.axis1, t1.axis2, t1.axis3, t1.artist, t1.title;
