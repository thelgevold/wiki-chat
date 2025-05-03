export class ChatImageResponse {
    constructor(public path: string, public description: string){}
}

export class ChatResponse {
    constructor(public role: string, public answer: string, public images: ChatImageResponse[], public children: ChatResponse[], public parent: ChatResponse|undefined){}
}