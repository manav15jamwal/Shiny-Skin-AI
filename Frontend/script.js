
        function handleAuth(e){
    e.preventDefault();

    if (isLogin){
        login();
    } else {
        register();
    }
}
        function openCart(){
    document.getElementById("cart-panel").classList.add("open");
    loadCart();   
}
function scrollToBottom(){
    const chatbox = document.getElementById("chat-box");

    setTimeout(() => {
        chatbox.scrollTop = chatbox.scrollHeight;
    }, 100);  
}
async function checkout(){
    document.getElementById("checkout-modal").style.display = "flex";

    lucide.createIcons();
    const token = localStorage.getItem("token");
    await fetch("http://backend:8000/cart/empty_cart",{
        method:"DELETE",
        headers:{
            "Authorization":"Bearer "+token
        },
        
    });
    document.getElementById("cart-items").innerHTML = "";
    document.getElementById("cart-summary").innerHTML = "";
    document.getElementById("cart-count").innerText = "0";
}
function closeCheckout(){
    document.getElementById("checkout-modal").style.display = "none";

    closeCart();   }
function showWelcome(name){
    const chatbox = document.getElementById("chat-box");

    const bot = document.createElement("div");
    bot.classList.add("bot");

    bot.innerHTML = `
        Hi ${name} <i data-lucide="smile"></i><br><br>
        Let’s take a quick skin test.<br><br>
        <button onclick="openCamera()">Start Test <i data-lucide="camera"></i></button>
    `;

    chatbox.appendChild(bot);
}
function closeCart(){
    document.getElementById("cart-panel").classList.remove("open");
}
        function showToast(message){
    const toast = document.getElementById("toast");

    toast.innerText = message;
    toast.style.opacity = "1";

    setTimeout(() => {
        toast.style.opacity = "0";
    }, 1500);
}
window.onload = async function() {
    const token = localStorage.getItem("token");

    lucide.createIcons();

    if (token) {

        try {
            const response = await fetch("http://backend:8000/auth/user", {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + token
                }
            });

            if (!response.ok) {
                logout();
                return;
            }

            document.getElementById("auth_section").style.display = "none";
            loadHistory();
            loadCart();

        } catch (error) {
            logout();
        }

    } else {
        renderBotMessage("Please Login.", true);
        document.getElementById("auth_section").style.display = "block";
    }
};
let lastScroll = 0;

const chatbox = document.getElementById("chat-box");


    function logout() {
    localStorage.removeItem("token");
    document.getElementById("auth_section").style.display = "block";
    const chatbox = document.getElementById("chat-box");
    const password = document.getElementById("password");
    password.innerText ="";
    chatbox.innerHTML="";
};
        let isLogin = true;
        function toggleAuth(){
            isLogin = !isLogin;

    const title = document.getElementById("auth-title");
    const toggleText = document.getElementById("toggle-text");
    const name = document.getElementById("name");
    const button = document.getElementById("login-button");
    const password = document.getElementById("password");

    const confirm_password = document.getElementById("confirm_password");
    

    if (isLogin){
        password.setAttribute("autocomplete", "current-password");
        title.innerText = "Login";
        name.style.display="none";
        confirm_password.style.display="none";
        button.onclick = login;
        toggleText.innerHTML = `Not a user? <span onclick="toggleAuth()">Register</span>`;
    } else {
        title.innerText = "Register";
        password.setAttribute("autocomplete", "new-password");
        name.style.display="block";
        confirm_password.style.display="block";
        button.onclick = register;

        toggleText.innerHTML = `Already a user? <span onclick="toggleAuth()">Login</span>`;
    }
}
    async function loadHistory(){
    const token = localStorage.getItem("token");

    try{
        const res = await fetch("http://backend:8000/chatbot/history",{
            headers:{
                "Authorization":"Bearer " + token
            }
        });

        const data = await res.json();

const chatbox = document.getElementById("chat-box");
chatbox.innerHTML = "";


if (data.history.length === 0){
    showWelcome(data.name);
    return;
}


data.history.reverse().forEach(chat => {


    let botText = "";

    try {
        const parsed = JSON.parse(chat.response);
        botText = parsed.message || "";
    } catch {
        botText = chat.response;
    }

   

renderUserMessage(chat.message);
renderBotMessage(botText,true);
    
}
);
scrollToBottom()
       

 } catch(e){
        console.error(e);
    }
}
function formatText(text){
    return text
        .replace(/\n/g, "<br>")               
        .replace(/(\d+\.)/g, "<br>$1")    
}
function renderUserMessage(text){
    const chatbox = document.getElementById("chat-box");

    const wrapper = document.createElement("div");
    wrapper.style.display = "flex";
    wrapper.style.justifyContent = "flex-end";

    const bubble = document.createElement("div");
    bubble.classList.add("user", "fade-in");
    bubble.innerText = text;

    wrapper.appendChild(bubble);
    chatbox.appendChild(wrapper);

    scrollToBottom();
}
async function renderBotMessage(text, instant=false){

    const chatbox = document.getElementById("chat-box");

    const wrapper = document.createElement("div");
    wrapper.style.display = "flex";
    wrapper.style.justifyContent = "flex-start";

    const bubble = document.createElement("div");
    bubble.classList.add("bot", "fade-in");

    wrapper.appendChild(bubble);
    chatbox.appendChild(wrapper);

    if (instant){
        bubble.innerText = text;
    } else {
        await typetext(bubble, text);
    }

    scrollToBottom();
}
    async function removeAll(productId){

    const token = localStorage.getItem("token");

    try{
        await fetch(
            `http://backend:8000/cart/remove_all/${productId}`,
            {
                method: "DELETE",
                headers: {
                    "Authorization": "Bearer " + token
                }
            }
        );

        showToast("Removed ❌");
        loadCart();

    } catch(error){
        console.error(error);
    }
}
    async function loadCart(){
    const token = localStorage.getItem("token");

    try{
        const response = await fetch("http://backend:8000/cart/my-cart", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        if (!response.ok){
            logout();
            return;
        }

        const data = await response.json();

        const container = document.getElementById("cart-items");
        container.innerHTML = "";
        document.getElementById("cart-count").innerText = data.length;
        let total = 0;
        data.forEach(item => {

            const div = document.createElement("div");
            div.classList.add("cart-item");
            
            div.innerHTML = `
    <div class="cart-row">

        <img src="${item.image_url}" class="cart-img"/>

        <div class="cart-info">
            <strong>${item.name}</strong>
            <p>Qty: ${item.quantity} | ₹${item.price * item.quantity}</p>

            <div class="cart-actions">
                <button onclick="removeFromCart(${item.product_id})">-</button>
                <button onclick="addtocart(${item.product_id})">+</button>
                <button onclick="removeAll(${item.product_id})">x</button>
            </div>
        </div>

    </div>
`;
            total += item.price*item.quantity;
            container.appendChild(div);
            


            lucide.createIcons();
        });const taxRate = 0.18;   

const tax = Math.round(total * taxRate);
const grandTotal = total + tax;

const summaryContainer = document.getElementById("cart-summary");

summaryContainer.innerHTML = `
    <div style="display:flex; justify-content:space-between;">
        <span>Subtotal</span>
        <span>₹${total}</span>
    </div>

    <div style="display:flex; justify-content:space-between;">
        <span>Tax (18%)</span>
        <span>₹${tax}</span>
    </div>

    <hr>

    <div style="display:flex; justify-content:space-between; font-size:16px;">
        <strong>Total</strong>
        <strong>₹${grandTotal}</strong>
    </div>

    <button style="width:100%; margin-top:10px;" onclick="checkout()">
        Buy Now
    </button>
`;    } catch(error){
        console.error(error);
    }
}
    async function removeFromCart(productId){

    const token = localStorage.getItem("token");

    try{
        const response = await fetch(
            `http://backend:8000/cart/remove/${productId}`,
            {
                method: "DELETE",
                headers: {
                    "Authorization": "Bearer " + token
                }
            }
        );

        if (!response.ok){
            logout();
            return;
        }

        showToast("Removed ❌");

        loadCart();  

    } catch(error){
        console.error(error);
    }
}
    async function register(){
        const name = document.getElementById("name").value;
        const password = document.getElementById("password").value;
        const confirm_password = document.getElementById("confirm_password").value;
        const email = document.getElementById("email").value;
        const confirmError = document.getElementById("confirm-error");

        confirmError.innerText = ""; 

        if (password !== confirm_password){
            confirmError.innerText = "Passwords do not match";
            return;
        }
    
        else{

            try{
                const response = await fetch("http://backend:8000/auth/register",{
                    method:"POST",
                    headers:{
                        "Content-type":"application/json"
                    },
                    body:JSON.stringify({
                        name:name,
                        password:password,
                        email:email

                    })
                });

                const data = await response.json();
                alert(data.message);
                if (data.message=="Registered successfully."){
                   login();
                };

            }
            catch(error){
                console.error(error);

            };
        };
        }
     
    
let stream;

async function openCamera() {
    const modal = document.getElementById("camera-modal");
    const video = document.getElementById("video");

    try {
        const permission = await navigator.permissions.query({ name: "camera" });

        if (permission.state === "denied") {
            alert("Camera access denied. Enable it from browser settings.");
            return;
        }

        modal.style.display = "flex";

        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;

    } catch (err) {
        console.error(err);
    }
}
function closeCamera() {
    const modal = document.getElementById("camera-modal");

    modal.style.display = "none";

    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
}

        function typetext(element, text, speed = 10){
    return new Promise(resolve => {

        let formatted = formatText(text);
        let i = 0;

        function typing(){
            if (i < formatted.length){
                element.innerHTML = formatted.slice(0, i);
                i++;
                setTimeout(typing, speed);
            } else {
                resolve();
                scrollToBottom();
            }
        }

        typing();
    });
}

        function renderProductsGroup(products){

    const chatbox = document.getElementById("chat-box");

    const wrapper = document.createElement("div");
    wrapper.style.display = "flex";
    wrapper.style.justifyContent = "flex-start";

    const bubble = document.createElement("div");
    bubble.classList.add("product-group");

    const list = document.createElement("div");
    list.classList.add("product-list");

    products.forEach(product => {

        const item = document.createElement("div");
        item.classList.add("product-item");

        item.innerHTML = `
            <img src="${product.image_url}" style="width:100%; border-radius:8px;" />
            <strong>${product.name}</strong>
            <p>₹${product.price}</p>
            <button onclick="addtocart(${product.id})">Add</button>
        `;

        list.appendChild(item);
    });
      bubble.appendChild(list);
    if (products.length >1){
        const addAllBtn = document.createElement("button");
    addAllBtn.innerText = "Add All 🛒";

    addAllBtn.onclick = () => {
        products.forEach(p => addtocart(p.id));
    };

  
    bubble.appendChild(addAllBtn);
    }

    wrapper.appendChild(bubble);
    chatbox.appendChild(wrapper);

    scrollToBottom();
}
            // const image = document.createElement("img");
            // img.src = product.image_url;
            // img.style.width = "100px";

           

            // const price = document.createElement("p");
            // typetext(price,"Rs."+product.price);

            
            // card.appendChild(image);
           
            // card.appendChild(price);
            
           
        
            
        
        function img2chat(img){
            const chatbox = document.getElementById("chat-box");
            const wrapper = document.createElement("div");
             wrapper.style.display = "flex";
            wrapper.style.justifyContent = "flex-end";

        const bubble = document.createElement("img");

            bubble.src = URL.createObjectURL(img);
            bubble.style.width ="150px";
            bubble.style.height ="220px";
            bubble.style.borderRadius = "10px";
        
        wrapper.appendChild(bubble);
        chatbox.appendChild(wrapper);

        scrollToBottom();
        return;

        }
        async function send_message(){
          
           const value = document.getElementById("input").value;
           if (!value) return;
           const chatbox = document.getElementById("chat-box");
           renderUserMessage(value);
           document.getElementById("input").value = "";
           const token = localStorage.getItem("token");
           const spinner = document.createElement("div");
            spinner.classList.add("spinner");

            const wrapper = document.createElement("div");
            wrapper.appendChild(spinner);
            chatbox.appendChild(wrapper);
           scrollToBottom()

           try{
            const response = await fetch("http://backend:8000/chatbot/chat",
            {
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization":"Bearer "+token        },
                body:JSON.stringify({
                    msg:value
                })
            }
        );
        if (!response.ok) {
            logout();

                }
        const data = await response.json();
        

const wrapper = document.createElement("div");
wrapper.style.display = "flex";
wrapper.style.justifyContent = "flex-start";

const bot = document.createElement("div");
spinner.remove();
await typetext(bot, data.message);
bot.classList.add("bot", "fade-in");

wrapper.appendChild(bot);
chatbox.appendChild(wrapper);   

await typetext(bot, data.message);
        

        if (data.products && data.products.length >0){
            renderProductsGroup(data.products);
        }
           }
        catch(error){
            const error_response = document.createElement("div");
            error_response.innerText = err;
            chatbox.appendChild(error_response);
    

        };

           

           scrollToBottom()


        }

        async function predict(file=None) {
             if (!file) {
            const fileinput = document.getElementById("fileinput");
            const file = fileinput.files[0];
    }
            const token = localStorage.getItem("token");

            if (!file) {
                alert("Upload a valid image first!!");
            return;}

            const formdata = new FormData();
            formdata.append("file",file);

            try{
                const response = await fetch("http://backend:8000/prediction/predict",{
                    method:"POST",
                    headers:{
                    "Authorization":"Bearer "+token           },
                    body:formdata
            
                    
                });
             const data = await response.json();
             if (data) {
                document.getElementById("input").value = "Took a test";
                img2chat(file);
                send_message()}

            }
            catch(error){
                return;
            }

        }
        const video = document.getElementById("video");
        async function capture() {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");

    const context = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(video, 0, 0);


    canvas.toBlob((blob) => {

        if (!blob) return;

        predict(blob);  

        closeCamera();
           

    }, "image/jpeg");


}

    async function addtocart(productId){

    const token = localStorage.getItem("token");

    try{
        const response = await fetch("http://backend:8000/cart/add", {
            method: "POST",
            headers: {
                "Content-Type":"application/json",
                "Authorization": "Bearer " + token
            },
            body:JSON.stringify(
                {product_id : productId}
            )
        });

        if (!response.ok){
            logout();
            return;
        }

        const data = await response.json();

        showToast("Added to cart ✅");
loadCart();

    } catch(error){
        console.error(error);
    }
}
            
        async function login() {
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            const formdata = new URLSearchParams();
            formdata.append("username",email);
            formdata.append("password",password);


            try{
                const response = await fetch("http://backend:8000/auth/token",{
                    method:"POST",
                    headers:{
                        "Content-type":"application/x-www-form-urlencoded"
                    },
                    body:formdata
                    })
                ;
                const data = await response.json();
                if (!data.access_token){
                    alert("Unauthorised access.");
                    return;
                };
                console.log(data);
                localStorage.setItem("token",data.access_token);
                document.getElementById("auth_section").style.display="none";

                    loadHistory();   
                    loadCart();      
                
            }
            catch(error){
                console.error(error);
            }
            
        }
 
const passwordInput = document.getElementById("password");
const confirmInput = document.getElementById("confirm_password");
const confirmError = document.getElementById("confirm-error");

confirmInput.addEventListener("input", () => {

    if (confirmInput.value !== passwordInput.value){
        confirmError.innerText = "Passwords do not match";

        confirmInput.classList.add("error-border");

    } else {
        confirmError.innerText = "";

        confirmInput.classList.remove("error-border");
    }

});
        function handleAuthEnter(e){
    if (e.key === "Enter"){
        if (isLogin){
            login();
        } else {
            register();
        }
    }
}

document.getElementById("email").addEventListener("keydown", handleAuthEnter);
document.getElementById("password").addEventListener("keydown", handleAuthEnter);
document.getElementById("confirm_password").addEventListener("keydown", handleAuthEnter);

document.getElementById("input").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey){
        e.preventDefault();
        send_message();
    }
});

       