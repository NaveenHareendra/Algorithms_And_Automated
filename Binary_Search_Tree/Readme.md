# CLRS Answer #Challenge
<ul>
 <li> This algorithm is an In-order tree walk procedure that is designed by me as an iterative method, using the sophisticated method using two pointers..</li>
 <li> I have also showed some possible design for iterative in order tree walk using "stacks".. which is quiet not bad too..
higher memory (stack method)> two pointer method</li>
 <li>check inorder_iterative.dscode for algorithm psuedocode; implementation can be found as:InOrderTreeWalkIterative(...) </li>
</ul>
 
This will run at O(m) average, don't consider to be the most efficient iterative method also, can be improved for sure as well.<br/>

At the end of the day best method :rescursive - Theta(n) time<br/><br/>
procedure (node)<br/>
  if node!=null<br/>
      procedure(node.left)<br/>
      print<br/>
      procedure(node.right)<br/>

