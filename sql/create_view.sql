create view mc
as
select m.axis1, m.axis2, m.axis3, a.name as "Artist", c.title, c.trackid, c.uri
  from coretracks c
  join coreartists a on a.artistid = c.artistid
  join musiccube m on m.trackid = c.trackid
