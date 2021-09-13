const signUp = document.querySelector('.sign-up');
const signIn = document.querySelector('.sign-in');


/*const btn1 = document.querySelector('.opposite-btn1');
const btn2 = document.querySelector('.opposite-btn2');*/

let x=document.createElement("input");
x.type="text";
x.name="name";
x.id="name";
x.placeholder="Name";
let y=document.createElement("input");
y.type="password";
y.name="confirm";
y.placeholder="Confirm Password";
// Switches to 'Create Account'
document.querySelector('.opposite-btn1').addEventListener('click', () => {
  signIn.querySelector('form').action="login";
  signIn.querySelector('.sign-in>h2').innerText="Sign Up";
  signIn.querySelector('form').insertBefore(x,signIn.querySelector('form').childNotes[0]);
  signIn.querySelector('form').appendChild(y);
  signIn.querySelector('form>p').className="opposite-btn2";
  signIn.querySelector('form>p').innerText="Already have an account?";
  /*signUp.style.display = 'block';
  signIn.style.display = 'none'; */
});

// Switches to 'Sign In'
document.querySelector('.opposite-btn2').addEventListener('click', () => {
  signIn.querySelector('form').action="signup";
  signIn.querySelector('.sign-in>h2').innerText="Sign In";
  signIn.querySelector('form').removeChild(x);
  signIn.querySelector('form').removeChild(y);
  signIn.querySelector('form>p').className="opposite-btn1";
  signIn.querySelector('form>p').innerText="Don't have an account?";
  /*signUp.style.display = 'none';
  signIn.style.display = 'block';*/
});signIn.querySelector('form').action="DifferentPythonFucntion";