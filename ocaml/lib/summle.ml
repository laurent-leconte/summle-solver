type op = Plus | Minus | Mul | Div

let int_of_op = function
  | Plus -> 0
  | Minus -> 1
  | Mul -> 2
  | Div -> 3

let string_of_op = function
  | Plus -> "+"
  | Minus -> "-"
  | Mul -> "*"
  | Div -> "/"

module Formula =
  struct
    type t = 
      | Leaf of int
      | Node of t * op * t
  let rec compare f1 f2 =
    match (f1, f2) with
      | Leaf(a), Leaf(b) -> Int.compare a b
      | Leaf(_), Node(_, _, _) -> -1
      | Node(_, _, _), Leaf(_) -> 1
      | Node(left1, op1, right1), Node(left2, op2, right2) ->
        let left_comp = compare left1 left2 in
        if left_comp <> 0 then left_comp
        else begin
          let op_comp = Int.compare (int_of_op op1) (int_of_op op2) in
          if op_comp <> 0 then op_comp
          else compare right1 right2
        end
  
  let rec num_steps = function
  | Leaf(_) -> 0
  | Node(l, _, r) -> 1 + num_steps l + num_steps r

  let to_string = 
    let rec aux add_paren = function
    | Leaf(a) -> string_of_int a
    | Node(l, o, r) -> 
        let template = format_of_string (if add_paren then "(%s %s %s)" else "%s %s %s") in
        Printf.sprintf template (aux true l) (string_of_op o) (aux true r) in
    aux false
  end

    
module Solution = 
  struct
    type t = {
    value: int;
    formula: Formula.t
  }
  let compare s1 s2 =
    let value_comp = Int.compare s1.value s2.value in
    if value_comp <> 0 then value_comp else Formula.compare s1.formula s2.formula 

  let from_int i = {value = i; formula = Leaf(i)}

  end

module Solutions = Set.Make(Solution)

let combinations l =
  let rec aux acc = function
    | [] | [_] -> acc
    | a::tl -> aux ((List.map (fun x -> (a,x)) tl)@acc) tl in
  aux [] l

  let split_map l =
    let rec aux beg acc = function
      | [] -> acc
      | a::tl -> let x = (List.rev beg)@tl in aux (a::beg) ((a,x)::acc) tl in
    aux [] [] l  

  let combinations_with_rest l =
    let rec aux acc prefix = function
      | [] -> List.rev acc
      | a::tl -> let x = split_map tl in
                 let rev_pref = List.rev prefix in
                 aux ((List.map (fun (b, rest) -> (a, b, rev_pref@rest)) x)@acc) (a::prefix) tl in
    aux [] [] l


let operations = [
  (Plus, (fun _  _ -> true), (+));
  (Minus, (fun x y -> x <> y), (-));
  (Mul, (fun _ y -> y <> 1), ( * ));
  (Div, (fun x y -> y > 1 && x mod y = 0), (/))
]

let rec apply_operations s1 s2 =
  let val1 = s1.Solution.value in
  let val2 = s2.Solution.value in
  let f (symbol, precond, op) =
    if precond val1 val2 then
      Some {Solution.value = (op val1 val2); Solution.formula = Node(s1.Solution.formula, symbol, s2.Solution.formula)}
    else None in
  if val1 < val2 
    then apply_operations s2 s1 
    else List.filter_map f operations

let generate_all inputs =
  let solutions = Hashtbl.create 128 in
  let add_to_hashtbl sol =
    let value = sol.Solution.value in
    match Hashtbl.find_opt solutions value with 
      | None -> Hashtbl.add solutions value (Solutions.singleton sol);
      | Some set -> Hashtbl.replace solutions value (Solutions.add sol set); in
  
  let rec aux = function
    | [] -> solutions
    | current::tl ->
        let apply_operations_and_fold to_append (s1, s2, rest) =
          (* generate all possible new values from s1 and s2 *)
          let new_solutions = apply_operations s1 s2 in
          (* add new solutions to the global solution hashtbl *)
          List.iter add_to_hashtbl new_solutions;
          (* append newly generated solutions and remainder to the queue,
            if there's at least one element in rest *)
          let new_queue = 
            if List.length rest > 0 
              then List.map (fun x -> x::rest) new_solutions
              else []
            in new_queue@to_append
        in (* end of apply_operations_and_fold *)
        let all_combinations = combinations_with_rest current in
        let new_tail = List.fold_left apply_operations_and_fold tl all_combinations in
        aux new_tail in
  
  aux [(List.map Solution.from_int inputs)]

let print_set = Solutions.iter (fun s -> print_endline @@ Formula.to_string s.formula)

let print_all =
  let print_one k s =
    Printf.printf "*** Solutions for %d ***\n" k;
    print_set s in
  Hashtbl.iter print_one

let count_all ht =
  let sum _ sols acc = acc + Solutions.cardinal sols in
  Hashtbl.fold sum ht 0

  let summle inputs =
    let start_time = Sys.time () in
    let all_solutions = generate_all inputs in
    let taken = Sys.time () -. start_time in
    Printf.printf "\n%d solutions computed in %.3f s\n" (count_all all_solutions) taken;
    all_solutions
