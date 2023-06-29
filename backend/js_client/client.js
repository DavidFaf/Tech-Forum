const contentContainer = document.getElementById('content-container')
const loginForm = document.getElementById('login-form')
const baseEndpoint = "http://localhost:8080/api"

if(loginForm) {
    loginForm.addEventListener('submit', handleLogin)
}

function handleLogin(event){
    console.log(event)
    event.preventDefault()
    const loginEndpoint = `${baseEndpoint}/token/`
    let loginFormData = new FormData(loginForm)
    let loginObjectData = Object.fromEntries(loginFormData)
    let loginDetails = JSON.stringify(loginObjectData)
    const options = {
        method : "POST",
        headers : {
            "Content-Type" : "application/json" 
        },
        body: loginDetails
    }

function fetchOptions(method, jsObject){
    return{
        method : method === null ? 'GET' : method, 
        headers : {
            "Content-Type" : "application/json" 
        },
        body: jsObject ? JSON.stringify(jsObject) : null
    }
}


async function fetchLoginData(){
    try {
    const response = await fetch(loginEndpoint, options)
    const data = await response.json()
    console.log(data)
    await fetchAuthData(data, fetchPosts)
    } catch (err) {
        console.log('err', err)
    }
        }

    fetchLoginData()

function fetchAuthData(authData, callback){
    localStorage.setItem('access', authData.access),
    localStorage.setItem('refresh', authData.refresh)
    
    if (callback){
        callback()
    }
    }

function writeToContainer(data){
    if (contentContainer){
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "</pre>" 
    }
}    

function isTokenValid(data){
    if (data.code === 'token_not_valid'){
        alert("please log in again")
        return false
    }
    return true
}

async function refreshJWTToken(refreshToken){
    try{
        const refreshEndpoint = `${baseEndpoint}/token/refresh/`
        const options = {
            method : "POST",
            headers : {
                "Content-Type" : "application/json" ,
            },
            body : JSON.stringify({
                refresh : refreshToken
            })
                }
        const response = await fetch(refreshEndpoint, options)
        const jsonData = await response.json()
        const refreshedToken = jsonData.access
        return refreshedToken
        } catch(err){
            console.log('err', err)
        }
}

async function validateJWTToken(){
    try{
        const verifyEndpoint = `${baseEndpoint}/token/verify/`
        const refreshToken = localStorage.getItem('refresh')
        const options = {
            method : "POST",
            headers : {
                "Content-Type" : "application/json" ,
                // "Authorization" : `Bearer ${localStorage.getItem('access')}`
            },
            body : JSON.stringify({
                token : localStorage.getItem('access')
            })
                }
        const response = await fetch(verifyEndpoint, options)
        const jsonData = await response.json()
        await refreshToken(refreshToken)
        } catch(err){
            console.log('err', err)
        }
}


async function fetchPosts(){
    try{
    const postEndpoint = `${baseEndpoint}/posts/`
    const options = {
        method : "GET",
        headers : {
            "Content-Type" : "application/json" ,
            // "Authorization" : `Bearer ${localStorage.getItem('access')}`
        }
            }
    const response = await fetch(postEndpoint, options)
    const jsonData = await response.json()
    const validToken = isTokenValid(jsonData)
    // refreshJWTToken(localStorage.getItem('refresh'))
    if (validToken) {
        await writeToContainer(jsonData)
    }
    } catch(err){
        console.log('err', err)
    }
}


}
    // fetch(loginEndpoint, options)
    // .then(
    //     response => {return response.json()}
    //     )
    // .then(authData)
    // .catch(err => {console.log('err', err)})

    
const searchClient = algoliasearch('A2VSEA6HSR', '6a6d985471dda823be818c77dc74e8d0');

const search = instantsearch({
    indexName: 'bigfafs_Post',
    searchClient,
});

search.addWidgets([
    instantsearch.widgets.searchBox({
    container: '#searchbox',
    }),

    instantsearch.widgets.clearRefinements({
        container: '#clear-refinements',
      }),
    

    instantsearch.widgets.refinementList({
        container: '#author-list',
        attribute: 'author',
      }),

    instantsearch.widgets.hits({
    container: '#hits',
    templates : {
        item : `<div>
        <div>{{#helpers.highlight}}{ "attribute": "title" }{{/helpers.highlight}}</div>
        <p>{{#helpers.highlight}}{ "attribute": "comment" }{{/helpers.highlight}}</p>
        <p>{{author}}</p>
        <p>{{comment_text}}</p>
        <div>`
    }
    })
]);

search.start();
