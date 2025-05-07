export class ChatResponse {
    constructor(public role: string, public content: string, public children: ChatResponse[], public parent: ChatResponse|undefined){}
}