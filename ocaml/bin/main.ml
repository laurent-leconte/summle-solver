
let run () = 
  for _ = 1 to 10 do
    let _ = Ocaml.Summle.summle [2; 3; 6; 7; 10; 75] in ()
  done

let start_time = Sys.time ()
let () = run ()
let tot_time = Sys.time() -. start_time
let () = Printf.printf "Total %.3f (avg %.3f)\n" tot_time (tot_time /. 10.)


